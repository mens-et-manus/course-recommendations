import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

# *****************
# set up data thing
# *****************

userIds = []
courses = []

names = ['user_id', 'item_id', 'rating'] # columns
df = pd.read_csv('test_data_1.csv', sep=',', names=names)
n_users = df.user_id.unique().shape[0] # get size
n_items = df.item_id.unique().shape[0]
ratings = np.zeros((n_users, n_items))
for row in df.itertuples():
	ratings[row[1]-1, row[2]-1] = row[3]
train = ratings

def getData(toFind, myData):

	# should input know, what you want to find

	# insert known data into the database

	user_similarity = fast_similarity(train, kind='user') # can use 'item' as well
	user_prediction = predict_topk(train, user_similarity, kind='user', k=10)
	print(user_prediction)

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

def predict_topk(ratings, similarity, kind='user', k=40):
    pred = np.zeros(ratings.shape)
    if kind == 'user':
        for i in range(0,ratings.shape[0]):
            top_k_users = [np.argsort(similarity[:,i])[:-k-1:-1]]
            for j in range(0,ratings.shape[1]):
                pred[i, j] = similarity[i, :][top_k_users].dot(ratings[:, j][top_k_users]) 
                pred[i, j] /= np.sum(np.abs(similarity[i, :][top_k_users]))
    if kind == 'item':
        for j in range(0,ratings.shape[1]):
            top_k_items = [np.argsort(similarity[:,j])[:-k-1:-1]]
            for i in range(0,ratings.shape[0]):
                pred[i, j] = similarity[j, :][top_k_items].dot(ratings[i, :][top_k_items].T) 
                pred[i, j] /= np.sum(np.abs(similarity[j, :][top_k_items]))        
    
    return pred


def addRowToKnown(row):
    row = row.split(",")
    _u = row[0].strip()
    userIds.append(_u)
    userIndex = len(userIds)-1
    # add a new row of zeroes with the width of the rest
    _d = row[1::]

    # TODO: finish this
    # modify "train" somehow

# ************
# predict it!
# ************
getData([
	{'user_id': 5, 'item_id': 3},
	{'user_id': 8, 'item_id': 4},
	{'user_id': 5, 'item_id': 4}
],[])