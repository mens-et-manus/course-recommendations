import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy

modelLoaded = False
r = []
SIMKEY = 'p:smlr:%s'
courses = []

def train(data_source):
	global courses
	global modelLoaded
	start = time.time()
	ds = pd.read_csv(data_source)
	print("Training data ingested in %s seconds." % (time.time() - start))
	start = time.time()
	courses = ds["course"].values.tolist()
	_train(ds)
	print("Engine trained in %s seconds." % (time.time() - start))
	modelLoaded = True

def _train(ds):
	tf = TfidfVectorizer(analyzer='word',
                         ngram_range=(1, 3),
                         min_df=0,
                         stop_words='english')
	tfidf_matrix = tf.fit_transform(ds['description'])

	cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

	for idx, row in ds.iterrows():
		similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
		similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

		# First item is the item itself, so remove it.
		# This 'sum' is turns a list of tuples into a single tuple:
		# [(1,2), (3,4)] -> (1,2,3,4)
		flattened = sum(similar_items[1:], ())
		r.append([SIMKEY % row['id'], *flattened])

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