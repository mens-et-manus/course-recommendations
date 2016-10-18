import json
text = ["id,description"]

with open('storage/classes.json') as data_file:    
    data = json.load(data_file)["courses"]
    counter = 1
    for course in data:
    	id = counter
    	counter = counter + 1
    	desc = "'".join(course["desc"].split("\""))
    	if desc == "":
    		desc = "Empty text. This is a test"
    	text.append(str(id) + ",\"" + desc + "\"")

text = "\n".join(text)
f = open('storage/classes.csv', 'w')
f.write(text)