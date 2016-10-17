#!/usr/bin/env python

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

# *****************
# set up data thing
# *****************

userIds = []
courses = []
n_users = 0
n_items = 0
train = np.zeros((n_users, n_items))

def predictData(newData):
    newData = newData.strip()
    index = addRowToKnown(newData)
    rowCopy = train[index]
	# should input know, what you want to find

    # insert known data into the database
    user_similarity = fast_similarity(train, kind='item') # can use 'item' as well
    user_prediction = predict_topk_nobias(train, user_similarity, kind='item', k=10)
    newRow = user_prediction[index]
    result = {}

    tot = 0
    num_tot = 0
    for i in range(0,len(rowCopy)):
        if rowCopy[i] != 0:
            tot = tot + (rowCopy[i] - newRow[i])
            num_tot = num_tot + 1
    avg = tot / num_tot

    for i in range(0,len(rowCopy)):
        if rowCopy[i] == 0 and newRow[i] != 0:
            # this was predicted!
            result[courses[i]] = round(newRow[i] + avg)
    return result

# ***************
# get similarity between users
# ***************

def fast_similarity(ratings, kind='user', epsilon=1e-9):
    # epsilon -> small number for handling dived-by-zero errors
    if kind == 'user':
        sim = ratings.dot(ratings.T) + epsilon
    elif kind == 'item':
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


def addRowToKnown(row):
    global n_users
    global n_items
    global train

    row = row.split(",")
    _u = row[0].strip()
    userIds.append(_u)
    userIndex = len(userIds)-1
    n_users = n_users+1
    # add a new row of zeroes with the width of the rest
    _d = row[1::]
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


f = open('collaborative_test.txt', 'r')
for line in f:
    addRowToKnown(line.strip())

# ************
# predict it!
# ************

# TODO: work on returning and adding relavant data
newKnownData = """
g,18.02 2,8.01 4,3.091 3
"""
result = predictData(newKnownData)
print(result)