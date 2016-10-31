from pymongo import MongoClient
client = MongoClient()
db = client.courses

def addToDB(id,courseList):
    newData = {
        "id": id,
        "courses": courseList
    }
    db.collab.insert_one(newData)

f = open('collaborative_test.txt', 'r')
for line in f:
    line = line.split(",")
    id = line[0]
    courseList = line[1::]
    addToDB(id,courseList)