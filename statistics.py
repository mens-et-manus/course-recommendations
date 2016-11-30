from pymongo import MongoClient
client = MongoClient()
db = client.courses

# db.queries
def queryMade(queryInfo):
	#
	newQuery = {
		"type": queryInfo["type"],
		"timestamp": queryInfo["timestamp"],
		"coursesInput": queryInfo["coursesInput"]
	}
	db.queries.insert(newQuery)

# db.predict
def courseUsedToPredict(courseInfo):
	# id and ratings
	
	# find if courseInfo.id exists in db.predict
	# if not, create w/ rating=rating num=1
	# if yes, update w/ num = num + 1, rating = ((rating*num) + rating)/(num+1)
	existing = cToArray(db.predict.find({
		"id": courseInfo["id"]
	}))
	if len(existing) > 0:
		# exists, update
		num = existing[0]["num"]
		rate = existing[0]["rating"]
		db.predict.update_one({
			"id": courseInfo["id"]
		},{
			"$set": {
				"num": num + 1,
				"rating": ((rate*num) + courseInfo["rating"])/(num+1)
			}
		})
	else:
		#
		db.predict.insert({
			"id": courseInfo["id"],
			"rating": courseInfo["rating"],
			"num": 1
		})

# db.predicted
def coursePredicted(id, rating=0):
	# id and rating (opt)
	existing = cToArray(db.predicted.find({
		"id": id
	}))
	if len(existing) > 0:
		# exists, update
		rate_num = existing[0]["rate_num"]
		rate = existing[0]["rating"]
		num = existing[0]["num"]
		db.predicted.update_one({
			"id": id
		},{
			"$set": {
				"rate_num": rate_num + 1,
				"num": num + 1,
				"rating": ((rate*rate_num) + rating)/(rate_num+1)
			}
		})
	else:
		#
		rate_num = 1
		if rating == 0:
			rate_num = 0
		db.predicted.insert({
			"id": id,
			"rating": rating,
			"rate_num": rate_num,
			"num": 1
		})

def getStats():
	ret = {}

	# highest rating (if has rating) in predicted
	maxPredictArr = cToArray(db.predict.find())
	maxPredict = None
	maxPredictIndex = -1
	for i in range(0,len(maxPredictArr)):
		if maxPredictIndex == -1 or maxPredictArr[i]["rating"] > maxPredictArr[maxPredictIndex]["rating"]:
			maxPredict = maxPredictArr[i]["id"]
			maxPredictIndex = i
	ret["max_predict_id"] = maxPredict
	ret["max_predict_rating"] = maxPredictArr[maxPredictIndex]["rating"]



	# highest rating in predict
	maxPredictArr = cToArray(db.predicted.find())
	maxPredict = None
	maxPredictIndex = -1
	maxPredictNum = None
	maxPredictNumIndex = -1
	for i in range(0,len(maxPredictArr)):
		if maxPredictIndex == -1 or maxPredictArr[i]["rating"] > maxPredictArr[maxPredictIndex]["rating"]:
			maxPredict = maxPredictArr[i]["id"]
			maxPredictIndex = i
		if maxPredictNumIndex == -1 or maxPredictArr[i]["num"] > maxPredictArr[maxPredictNumIndex]["num"]:
			maxPredictNum = maxPredictArr[i]["id"]
			maxPredictNumIndex = i
	ret["max_predicted_id"] = maxPredict
	ret["max_predicted_rating"] = maxPredictArr[maxPredictIndex]["rating"]
	ret["max_predicted_num_id"] = maxPredictNum
	ret["max_predicted_num"] = maxPredictArr[maxPredictNumIndex]["num"]

	# most common in predict/predicted

	ret["evals"] = len(list(db.evals.find({})))


	# number of queries
	ret["queries"] = cToArray(db.queries.find({
		"type": "get"
	}))
	ret["queries"] = len(ret["queries"])
	return ret;

def cToArray(c):
	arr = []
	for _c in c:
		arr.append(_c)
	return arr