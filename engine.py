#!/usr/bin/env python

import numpy as np
import pandas as pd
import sklearn 
from sklearn.metrics import mean_squared_error
from pymongo import MongoClient
client = MongoClient()
db = client.courses

import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn import preprocessing
import json
import statistics

#                  id = uuid
#                  courseList = ["id rating","id rating"...]
#                  courses = [id, id, ...]
def combinePredict(id, courseList, courses, prefered):
    # this one is easy
    collab_result = predictCollab(id, courseList)
    # make an array of the input ratings
    course_ratings = []
    for item in courseList:
        i = item.split(" ")
        course_ratings.append(int(i[1]))
    # get all of the similarities
    content_result_temp = []
    for course in courses:
        predictions = predictContent(course)
        content_result_temp.append(predictions)
    # sum them up for each id
    content_result = {}
    for i in range(0, len(content_result_temp)):
        row = content_result_temp[i]
        # get ratings here, I guess...somehow
        for item in row:
            if (item["id"] in content_result) == False:
                content_result[item["id"]] = {
                    "num": 0,
                    "tot_rating": []
            }
            content_result[item["id"]]["num"] = content_result[item["id"]]["num"] + item["num"]
            content_result[item["id"]]["tot_rating"].append(course_ratings[i])
    # get the average rating
    for item in content_result:
        _s = 0
        for rating in content_result[item]["tot_rating"]:
            _s = _s + rating
        if len(content_result[item]["tot_rating"]) > 0:
            _s = _s / len(content_result[item]["tot_rating"])
        content_result[item]["tot_rating"] = _s

    # now we just have to normalize the nums

    # test normalization here
    norm_nums = []
    norm_ids = []
    norm_tot = []
    norm_ratings = []
    for item in content_result:
        norm_nums.append(content_result[item]["num"])
        norm_tot.append(content_result[item]["tot_rating"])
        norm_ids.append(item)
    norm_nums = preprocessing.normalize([norm_nums], norm='l2')[0]
    for i in range(0,len(norm_nums)):
        norm_ratings.append(norm_tot[i] * norm_nums[i])
    norm_ratings = sklearn.preprocessing.minmax_scale(np.array(norm_ratings),feature_range=(1,5))
    for i in range(0,len(norm_ids)):
        id = norm_ids[i]
        content_result[id]["rating"] = norm_ratings[i]

    #instructor ratings: course[year][season]["instructors"][each][stats][rating]
    #assignments contributed to learning: course[year][season]["stats"]["assignments"]["avg"]
    #student learning objectives were met : course[year][season]["stats"]["objectives"]["avg"]
    #subject expectations met : course[year][season]["stats"]["expect"]["avg"]
    #grading was fair: course[year][season]["stats"]["grading"]["avg"]
    #pace of the class: course[year][season]["stats"]["pace"]["avg"]
    #hours inside class: : course[year][season]["stats"]["inside"]["avg"]
    #hours outside class: : course[year][season]["stats"]["outside"]["avg"]
    #rating: : course[year][season]["stats"]["rating"]["avg"]
    
    # compile the results
    tot_result_dict = {}
    for item in content_result:
        if (item in tot_result_dict) == False:
            tot_result_dict[item] = {}
        tot_result_dict[item]["content"] = content_result[item]["rating"]
    for item in collab_result:
        if (item in tot_result_dict) == False:
            tot_result_dict[item] = {}
        tot_result_dict[item]["collab"] = collab_result[item]
    for item in tot_result_dict:
        id = item
        evalData = getEvalData(id)
        if evalData != None:
            tot_result_dict[item]["eval_rating"] = evalData["combined"]["rating"]
            if prefered in evalFields:
                tot_result_dict[item]["eval_pref"] = evalData["combined"][prefered]

    # average them
    tot_result = []
    for item in tot_result_dict:
        _s = 0
        _l = 0
        for rating in tot_result_dict[item]:
            _s = _s + tot_result_dict[item][rating]
            _l = _l + 1
        if _l != 0:
            tot_result.append({
                "id": item,
                "rating": _s/_l,
                "stats": statistics.evalStats(item)
            })
    # sort dictionary by rating

    tot_result.sort(key=lambda x:x['rating'])
    tot_result.reverse()
    return tot_result

    # id: uuid
    # courselist: list of courses
    # 1. get predicted ratings EVERY course
    # 2. for EVERY course, get sum of similarity between it and all other supplied courses

#=========================
#
# EVAL
#
#
#=====================
evalFields = ["instructors","assignments","objectives","expect","grading","pace","inside","outside","rating"] # should be averaged, can be set as "prefered"

def getEvalData(id):
    ret = {
        "combined": None,
        "raw": None
    }
    results = list(db.evals.find({
        "id": id
    }))
    if len(results) == 0:
        return None
    #
    # AVERAGE INSTRUCTOR RATINGS
    #
    for i in range(0,len(results)):
        if "_id" in results[i]:
            del results[i]["_id"]
        avg = []
        instructors = results[i]["instructors"]
        for instructor in instructors:
            avg.append(instructor["stats"]["rating"])
        if len(avg) == 0:
            avg = 0
        else:
            avg = np.sum(avg)/len(avg)
        results[i]["stats"]["instructors"] = {"avg":avg}
    ret["raw"] = results
    #
    # GET AVERAGES
    #
    #
    averages = {}
    for field in evalFields:
        averages[field] = []
        for result in results:
            averages[field].append(result["stats"][field]["avg"])
        if len(averages[field]) == 0:
            averages[field] = 0
        else:
            averages[field] = np.sum(averages[field])/len(averages[field]) * (5/7)
    ret["combined"] = averages
    return ret


#=========================
#
# COLLABORATIVE
#
#=========================



# *****************
# set up data thing
# *****************

userIds = []  # a list of all of the user ids that are currently in the matrix
coursesCollab = []  # a list of all the courses '''''
n_users = 0   # length of the array userIds
n_items = 0   # length of the array courses
trainCollab = np.zeros((n_users, n_items))  # initializes the matrix (empty for now)

def predictData(newData,id,courseList):
    newData = newData.strip()           # removes whitespace
    index = addRowToKnown(id,courseList)      # add to the matrix, returns the index (row) where the data will be once predicted
    rowCopy = trainCollab[index]
    user_similarity = fast_similarity(trainCollab, kind='item') # finds the similarity coefficient (math stuff)
    user_prediction = predict_topk_nobias(trainCollab, user_similarity, kind='item', k=10) # turns the similarity into predicted ratings (more math)
    newRow = user_prediction[index] # get the predicted row
    result = {}                     # what will eventually be returned

    tot = 0                         # calculates the average error
    num_tot = 0                     # counter to eventually divide the total be
    for i in range(0,len(rowCopy)):   # go through each item in row
        if int(rowCopy[i]) != 0:           # if it was not predicted...
            tot = tot + (rowCopy[i] - newRow[i])    # find the difference between the result and the actual result
            num_tot = num_tot + 1                   # increment the counter
    avg = tot / num_tot     # calculate the average error
    for i in range(0,len(rowCopy)):
        if (rowCopy[i]) == 0 and (newRow[i]) != 0:
            result[coursesCollab[i]] = round(newRow[i] + avg) # accounts for average error to get a better prediction
    return result       # returns predictions

# ***************
# get similarity between users
# ***************

def fast_similarity(ratings, kind='user', epsilon=1e-9):
    # epsilon -> small number for handling dived-by-zero errors
    if kind == 'user':
        sim = ratings.dot(ratings.T) + epsilon          # predict by similar users (using this)
    elif kind == 'item':                                # predict by similar items
        sim = ratings.T.dot(ratings) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

# *************
# predict while only taking k users into account (the most similar)
# *************

def predict_topk_nobias(ratings, similarity, kind='user', k=40):
    pred = np.zeros(ratings.shape)
    if kind == 'user':
        user_bias = ratings.mean(axis=1)
        ratings = (ratings - user_bias[:, np.newaxis]).copy()
        for i in range(0,ratings.shape[0]):
            top_k_users = [np.argsort(similarity[:,i])[:-k-1:-1]]
            for j in range(0,ratings.shape[1]):
                pred[i, j] = similarity[i, :][top_k_users].dot(ratings[:, j][top_k_users]) 
                pred[i, j] /= np.sum(np.abs(similarity[i, :][top_k_users]))
        pred += user_bias[:, np.newaxis]
    if kind == 'item':
        item_bias = ratings.mean(axis=0)
        ratings = (ratings - item_bias[np.newaxis, :]).copy()
        for j in range(0,ratings.shape[1]):
            top_k_items = [np.argsort(similarity[:,j])[:-k-1:-1]]
            for i in range(0,ratings.shape[0]):
                pred[i, j] = similarity[j, :][top_k_items].dot(ratings[i, :][top_k_items].T) 
                pred[i, j] /= np.sum(np.abs(similarity[j, :][top_k_items])) 
        pred += item_bias[np.newaxis, :]
        
    return pred


def addRowToKnown(id,courseList):
    global n_users
    global n_items
    global trainCollab
    
    _u = id
    userIds.append(_u)
    userIndex = len(userIds)-1
    n_users = n_users+1
    # add a new row of zeroes with the width of the rest
    _d = courseList
    # go through courses
    for course_rating in _d:
        info = course_rating.split(" ")
        course = info[0]
        if (course in coursesCollab) == False:
            coursesCollab.append(course)
            n_items = n_items+1

    # CREATE NEW ARRAY
    new_ratings = np.zeros((n_users, n_items))
    # COPY OVER ALL EXISTING DATA
    for i in range(0,trainCollab.shape[0]):
        for j in range(0,trainCollab.shape[1]):
            new_ratings[i][j] = trainCollab[i][j]

    for course_rating in _d:
        info = course_rating.split(" ")
        course = info[0]
        rating = int(info[1])
        courseIndex = coursesCollab.index(course)
        new_ratings[userIndex][courseIndex] = rating
    trainCollab = new_ratings
    return userIndex

def addToDB(id,courseList):
    newData = {
        "id": id,
        "courses": courseList
    }
    db.collab.insert(newData)


def predictCollab(id,courseList):
    text = id + "," + ",".join(courseList)
    addToDB(id,courseList)
    result = predictData(text,id,courseList)
    return result

#
# INITIALIZE
#

entries = db.collab.find()
for entry in entries:
    id = entry["id"]
    courseList = entry["courses"]
    addRowToKnown(id,courseList)

#============================
#
# CONTENT
#
#
#==============================

modelLoaded = False     # stores whether or not the machine learning model is ready to use
r = []                  # just an array to store the results
SIMKEY = 'p:smlr:%s'    # stores the id; not really important
coursesContent = []            # stores the list of possible courses

def trainContent(data_source):
    global coursesContent          # makes sure these are global variables
    global modelLoaded      # ''''
    start = time.time()     # times how long it takes to train the model
    ds = pd.DataFrame(data_source)   # gets the information from the csv (in this case /static/storage/classes.csv)
    print("Training data ingested in %s seconds." % (time.time() - start))
    start = time.time()
    coursesContent = ds["id"].values.tolist()  # turns the csv data into an array
    _trainContent(ds)                              # trains the model
    print("Engine trained in %s seconds." % (time.time() - start))
    modelLoaded = True          # ready to go!

def _trainContent(ds):
    tf = TfidfVectorizer(analyzer='word',           # sets up the matrix (math stuff)
                         ngram_range=(1, 3),
                         min_df=0,
                         stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['desc'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    for idx, row in ds.iterrows():      # goes through all the courses
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

        # First item is the item itself, so remove it.
        # This 'sum' is turns a list of tuples into a single tuple:
        # [(1,2), (3,4)] -> (1,2,3,4)
        flattened = sum(similar_items[1:], ())
        r.append([SIMKEY % row['id'], *flattened])      # appends the list of similar courses to a particular course

def predictContent(course_id, num=20):
    global coursesContent
    item_id = 1 + coursesContent.index(course_id)
    for i in range(0,len(r)):
        if r[i][0] == SIMKEY % course_id:
            arr= r[i][1:num-1]
            odd = arr[1::2]
            even = arr[::2]
            ret = []
            for j in range(0,len(odd)):
                ret.append({
                    "id": odd[j],
                    "num": even[j]
                })
            return ret

def modelReady():
    return modelLoaded

# initializing the model

arr = []
allDescs = db.courses.find()
for item in allDescs:
    arr.append({
        "id": item["id"],
        "title": item["title"],
        "desc": item["desc"]
    })
trainContent(arr)