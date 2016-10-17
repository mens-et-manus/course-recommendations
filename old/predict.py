import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt

header = ['user_id', 'item_id', 'rating']
df = pd.read_csv('test_data_1.csv', sep=',', names=header)

n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]

from sklearn import cross_validation as cv
train_data, test_data = cv.train_test_split(df, test_size=0)

print(train_data)

train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
    train_data_matrix[line[1]-1, line[2]-1] = line[3]  

from sklearn.metrics.pairwise import pairwise_distances
user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')

def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis]) 
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])     
    return pred

user_prediction = predict(train_data_matrix, user_similarity, type='user')

'''
5 -> 1
4 -> 2
3 -> 3
2 -> 4
5 -> 1

actual = 6 - observed
'''

def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten() 
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))

def getResult(user_id, test_id):
	myData = [
		{'user_id': user_id, 'item_id': test_id-1, 'rating': 0 },
		{'user_id': user_id, 'item_id': test_id, 'rating': 0 } # some junk rating value
	]
	d = pd.DataFrame(myData)
	test_data_matrix = np.zeros((n_users, n_items))
	for line in d.itertuples():
	    test_data_matrix[line[1]-1, line[2]-1] = line[3]
	print('User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix)))
	for data in myData:
		print(5-round(user_prediction[data['user_id']-1][data['item_id']-1]))

getResult(5,4)
