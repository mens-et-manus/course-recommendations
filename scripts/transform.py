#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

def getRows(row):
	year = row[0]
	major = row[1]
	liked = row[2].split("|")
	for i in range(0,len(liked)):
		liked[i] = liked[i].strip()
		liked[i] = liked[i].split(" ")
	ret = []
	for i in range(0,len(liked)):
		for j in range(0,len(liked)):
			if i != j:
				course1 = liked[i][0]
				teacher1 = liked[i][1]
				course2 = liked[j][0]
				teacher2 = liked[j][1]
				ret.append([year,major,course1,teacher1,course2,teacher2])
				ret.append([year,major,course2,teacher2,course1,teacher1])
	return ret;

# year, major, liked course 1, liked teacher 1, liked course 2, liked teacher 2
with open('sample_data.csv', 'rt') as csvfile1:
	reader = csv.reader(csvfile1, delimiter=',', quotechar='/')
	with open('sample_data_transformed.csv', 'wt') as csvfile2:
		writer = csv.writer(csvfile2, delimiter=',', quotechar='/', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['year','major','course1','teacher1','course2','teacher2'])
		for row in reader:
			rows = getRows(row)
			for _row in rows:
				writer.writerow(_row)