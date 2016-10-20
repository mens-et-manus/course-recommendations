import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy

modelLoaded = False		# stores whether or not the machine learning model is ready to use
r = []					# just an array to store the results
SIMKEY = 'p:smlr:%s'	# stores the id; not really important
courses = []			# stores the list of possible courses

def train(data_source):
	global courses			# makes sure these are global variables
	global modelLoaded		# ''''
	start = time.time()		# times how long it takes to train the model
	ds = pd.read_csv(data_source)	# gets the information from the csv (in this case /static/storage/classes.csv)
	print("Training data ingested in %s seconds." % (time.time() - start))
	start = time.time()
	courses = ds["course"].values.tolist()	# turns the csv data into an array
	_train(ds)								# trains the model
	print("Engine trained in %s seconds." % (time.time() - start))
	modelLoaded = True			# ready to go!

def _train(ds):
	tf = TfidfVectorizer(analyzer='word',			# sets up the matrix (math stuff)
                         ngram_range=(1, 3),
                         min_df=0,
                         stop_words='english')
	tfidf_matrix = tf.fit_transform(ds['description'])
	cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
	for idx, row in ds.iterrows():		# goes through all the courses
		similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
		similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

		# First item is the item itself, so remove it.
		# This 'sum' is turns a list of tuples into a single tuple:
		# [(1,2), (3,4)] -> (1,2,3,4)
		flattened = sum(similar_items[1:], ())
		r.append([SIMKEY % row['id'], *flattened])		# appends the list of similar courses to a particular course

def predict(course_id, num=10):
	global courses
	item_id = 1 + courses.index(course_id)
	for i in range(0,len(r)):
		if r[i][0] == SIMKEY % item_id:
			arr= r[i][1:num-1]
			odd = arr[1::2]
			even = arr[::2]
			ret = []
			for j in range(0,len(odd)):
				ret.append({
					"id": courses[odd[j]-1],
					"num": even[j]
				})
			return ret

def modelReady():
	return modelLoaded

train('static/storage/classes.csv')