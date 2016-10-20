import json
text = ["id,description,course"]

with open('static/storage/classes.json') as data_file:    
    data = json.load(data_file)["courses"]
    counter = 1
    for course in data:
    	id = counter
    	counter = counter + 1
    	desc = "'".join(course["desc"].split("\""))
    	if desc == "":
    		desc = "No description"
    	cid = course["id"]
    	text.append((str(id) + ",\"" + desc + "\",\"" + cid + "\"").encode("utf-8"))

text = "\n".join(text)
f = open('static/storage/classes.csv', 'w')
f.write(text)