# course-recommendations
Course recommendations using AI

## Setup
```
pip3 install -r requirements.txt
# install redis somehow (brew, apt, etc.)
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

### TODO
+ set up databases and stuff
+ add collaborative-based recommendations
	+ get sample data
