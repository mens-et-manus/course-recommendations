from flask import Flask, render_template, request, jsonify
import json
import uuid
import content
import collaborative

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
 
@app.route('/')
def index(user=None):
    return render_template('index.html')

@app.route('/about')
def about(user=None):
    return render_template('about.html')

@app.route('/predict/all', methods=['POST'])
def predictAll():
	data = request.json
	#
	# CONTENT-BASED
	#
	courses = data["courses"]
	rate = data["ratings"]
	ret = []
	for course in courses:
		if content.modelReady() == True:
			predictions = content.predict(course)
			ret.append(predictions)
	#
	# COLLAB
	#
	id = data["id"]
	courseList = data["courseList"]
	for i in range(0,len(courseList)):
		courseList[i] = str(courseList[i][0]) + " " + str(courseList[i][1])
	predictData = collaborative.predictCollab(id,courseList)


	return jsonify({
		"content": {
			"data": ret,
			"courses": courses,
			"ratings": rate
		},
		"collab": {
			"data": predictData
		}
	})

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run()

def generateId():
	return str(uuid.uuid1())