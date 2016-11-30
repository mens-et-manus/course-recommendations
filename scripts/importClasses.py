import json
from pymongo import MongoClient
client = MongoClient()
db = client.courses

with open('../static/storage/classes.json','r') as infile2:
	if2 = infile2.read()
	if if2 == "":
		if2 = "{}"
	data = json.loads(if2)["courses"]

	for item in data:
		new_data = {
			"id": item["id"],
			"title": item["title"],
			"desc": item["desc"]
		}
		db.courses.insert(new_data)