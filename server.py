from flask import Flask, render_template, request, jsonify
import json
import uuid
import content
 
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

@app.route('/predict/content', methods=['POST'])
def predictContent():
	data = request.json
	courses = data["courses"]
	rate = data["ratings"]
	ret = []
	for course in courses:
		if content.modelReady() == True:
			predictions = content.predict(course)
			ret.append(predictions)
	# return the stuff here
	return jsonify({
		"data": ret,
		"courses": courses,
		"ratings": rate
	})

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run()

def generateId():
	return str(uuid.uuid1())