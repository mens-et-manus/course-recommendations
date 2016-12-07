# course-recommendations
Course recommendations using AI

## Installation

### Requirements
+ Nginx
+ Python3 + Pip3
+ MongoDB
+ `uwsgi-core` and `uwsgi-plugin-python3`

### Install Python requirements
```
sudo apt-get install python-qt4 qt4-dev-tools
pip3 install -r requirements.txt
uwsgi --ini courserecs.ini --plugin python3 --chmod-socket=666
```

## Types of Prediction
We will be using a combination of the the following 2 methods:

### Collaborative Filtering
Looks at the ratings of other users and uses their similarity to the input user to predict their ratings for courses.
+ **Pros:** Easy to implement, fast
+ **Cons:** Requires lots of collected data to be effective

### Content-Based Prediction
Gets similar courses based on the course descriptions. Uses language processing to compare the text
+ **Pros:** Easy to scrape data
+ **Cons:** Only gets courses that _sound_ similar

## Database
```
db -> courses
db.collab
db.predict
db.queries
db.predicted

```

### Global Stats
+ Highest predicted rating
+ Most liked (input)
+ Most predicted
+ Number of queries

```
sudo uwsgi --http-socket :5000 --plugin python3 --wsgi-file wsgi.py
```