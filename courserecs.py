from flask import Flask, render_template, request, jsonify
import json
import uuid
#import content
#import collaborative
import engine
import statistics
import flask_login
from datetime import datetime
#
# SETUP
#

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
 
#
# PAGES
#
#

@app.route('/recommend')
def index(user=None):
	return render_template('index.html')

@app.route('/')
def about(user=None):
    return render_template('about.html')

#
# DATA
#
#

@app.route('/predict/all', methods=['POST'])
def predictAll():
	data = request.json
	#
	# CONTENT-BASED
	#
	courses = data["courses"]
	rate = data["ratings"]

	# statistics information
	statistics.queryMade({
		"type": "get",
		"timestamp": datetime.utcnow(),
		"coursesInput": courses
	})

	#
	# COLLAB
	#
	id = data["id"] # TODO: generate this....
	courseList = data["courseList"]
	for i in range(0,len(courseList)):
		# stats
		statistics.courseUsedToPredict({
			"id": courseList[i][0],
			"rating": courseList[i][1]
		})
		courseList[i] = str(courseList[i][0]) + " " + str(courseList[i][1])


	fullRes = engine.combinePredict(id, courseList, courses, "instructors")

	#
	# STATS
	#

	for item in fullRes:
		statistics.coursePredicted(item["id"],rating=item["rating"])

	return jsonify({
		"full": {
			"data": fullRes
		}
	})

#
# STATS
#
@app.route('/stats', methods=['GET'])
def getStats():
	stats = statistics.getStats();
	return jsonify(stats)

#
# USERS
#
#



#
# STATIC
#
#

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

if __name__ == '__main__':
	app.run(host='0.0.0.0')

def generateId():
	return str(uuid.uuid1())
