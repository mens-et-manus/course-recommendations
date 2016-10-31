#!/usr/bin/env python

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from pymongo import MongoClient
client = MongoClient()
db = client.courses

# *****************
# set up data thing
# *****************

userIds = []  # a list of all of the user ids that are currently in the matrix
courses = []  # a list of all the courses '''''
n_users = 0   # length of the array userIds
n_items = 0   # length of the array courses
train = np.zeros((n_users, n_items))  # initializes the matrix (empty for now)

def predictData(newData,id,courseList):
    newData = newData.strip()           # removes whitespace
    index = addRowToKnown(id,courseList)      # add to the matrix, returns the index (row) where the data will be once predicted
    rowCopy = train[index]

    user_similarity = fast_similarity(train, kind='item') # finds the similarity coefficient (math stuff)
    user_prediction = predict_topk_nobias(train, user_similarity, kind='item', k=10) # turns the similarity into predicted ratings (more math)
    newRow = user_prediction[index] # get the predicted row
    result = {}                     # what will eventually be returned

    tot = 0                         # calculates the average error
    num_tot = 0                     # counter to eventually divide the total be
    for i in range(0,len(rowCopy)):   # go through each item in row
        if rowCopy[i] != 0:           # if it was not predicted...
            tot = tot + (rowCopy[i] - newRow[i])    # find the difference between the result and the actual result
            num_tot = num_tot + 1                   # increment the counter
    avg = tot / num_tot     # calculate the average error

    for i in range(0,len(rowCopy)):
        if rowCopy[i] == 0 and newRow[i] != 0:
            result[courses[i]] = abs(round(newRow[i] + avg)) % 5 # accounts for average error to get a better prediction
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
    global train
    
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
        if (course in courses) == False:
            courses.append(course)
            n_items = n_items+1

    # CREATE NEW ARRAY
    new_ratings = np.zeros((n_users, n_items))
    # COPY OVER ALL EXISTING DATA
    for i in range(0,train.shape[0]):
        for j in range(0,train.shape[1]):
            new_ratings[i][j] = train[i][j]

    for course_rating in _d:
        info = course_rating.split(" ")
        course = info[0]
        rating = int(info[1])
        courseIndex = courses.index(course)
        new_ratings[userIndex][courseIndex] = rating

    train = new_ratings
    return userIndex

def addToDB(id,courseList):
    newData = {
        "id": id,
        "courses": courseList
    }
    db.collab.insert_one(newData)


def predictCollab(id,courseList):
    text = id + "," + ",".join(courseList)
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


#
#   LOAD SOME SAMPLE DATA
#

"""
newKnownData = "g,18.02 2,8.01 4,3.091 3"
result = predictData(newKnownData)
print(result)
"""