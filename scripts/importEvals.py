import json
from pymongo import MongoClient
client = MongoClient()
db = client.courses

with open('../static/storage/allEval.json','r') as infile2:
	if2 = infile2.read()
	if if2 == "":
		if2 = "{}"
	data = json.loads(if2)

	for id_key in data:
		for year_key in data[id_key]:
			for season_key in data[id_key][year_key]:
				item = data[id_key][year_key][season_key]
				# .instructors
				# .stats
				# .summary
				newData = {
					"id": id_key,
					"year": year_key,
					"season": season_key,
					"instructors": item["instructors"],
					"stats": item["stats"],
					"summary": item["summary"]
				}
				db.evals.insert(newData)