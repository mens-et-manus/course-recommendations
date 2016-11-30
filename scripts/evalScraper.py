import urllib.request
import uuid
import re
import json
import subprocess

start = "https://edu-apps.mit.edu/ose-rpt/"

ret = {}
num = 0
count = 0

getTitle = re.compile(b'<title>(.*?)<\/title>', re.S)
getSummary = re.compile(b'<table class="summary">(.*?)<\/table>', re.S)
getGrid = re.compile(b'<table(.*?)class="grid">(.*?)<\/table>', re.S)
getTables = re.compile(b'<table cellspacing="0" cellpadding="0" border="0" class="indivQuestions">.*?<\/table>', re.S)
getMeans = re.compile(b'<table cellspacing="0" cellpadding="0" style="width: 70px;" class="mean">.*?<\/table>', re.S)
getBars = re.compile(b'<table style="width: 70px;" class="barheader">.*?<\/table>', re.S)
def parseTitle(title):
	title = title[0].decode("utf-8").split(" ")
	year = title[4]
	season = title[3]
	ids = title[2].split("/")
	return {
		"year": year,
		"season": season,
		"ids": ids
	}

def parseTables(table):
	getTrs = re.compile(b'<tr>(.*?)<\/tr>', re.S)

	table1 = getTrs.findall(table[0])
	table2 = getTrs.findall(table[1])
	table3 = getTrs.findall(table[2])
	table4 = getTrs.findall(table[3])
	stats = {
		"expect": parseTr(table1[3]),
		"objectives": parseTr(table1[4]),
		"assignments": parseTr(table1[5]),
		"grading": parseTr(table1[6]),
		"pace": parseTr(table2[3]),
		"inside": parseTr(table3[3]),
		"outside": parseTr(table3[4]),
		"rating": parseTr(table4[3])
	}
	return stats

def parseSummary(summary):
	summary = summary[0]
	getPossible = re.compile(b'Eligible to Respond:</strong>(.*?)<', re.S)
	getDid = re.compile(b'Total # of Respondents:</strong>(.*?)<', re.S)
	getRate = re.compile(b'Response rate:</strong>(.*?)%', re.S)
	getRating = re.compile(b'Overall rating of subject: </strong>(.*?)out', re.S)

	possible = float(getPossible.findall(summary)[0].strip())
	did = float(getDid.findall(summary)[0].strip())
	rate = float(getRate.findall(summary)[0].strip())
	rating = float(getRating.findall(summary)[0].strip())

	return {
		"possible": possible,
		"did": did,
		"rate": rate,
		"rating": rating
	}

def parseTr(tr):
	getTd = re.compile(b'<td(.*?)>(.*?)<\/td>', re.S)
	tds = getTd.findall(tr)
	#rint(tds)
	stats = {
		"avg": float(tds[1][1].decode("utf-8")),
		"num": float(tds[3][1].decode("utf-8")),
		"median": float(tds[4][1].decode("utf-8")),
		"std": float(tds[5][1].decode("utf-8"))
	}
	return stats

def parseInst(grid):
	inst = []
	grid = grid[0][1]

	getTrs = re.compile(b'<tr>(.*?)<\/tr>', re.S)
	getId = re.compile(b'instructorId=(.*?)\&', re.S)
	getName = re.compile(b'<strong>(.*?),(.*?)<\/strong>', re.S)
	getPosition = re.compile(b'<\/a>(.*?)<span', re.S)
	getAvgs = re.compile(b'<span class="avg">(.*?)<\/span>', re.S)

	trs = getTrs.findall(grid)
	for i in range(2,len(trs)):
		tr = trs[i]
		id = getId.findall(tr)[0].strip().decode("utf-8")
		name = getName.findall(tr)
		name = name[0][1].strip().decode("utf-8") + " " + name[0][0].strip().decode("utf-8")
		position = getPosition.findall(tr)[0].strip().decode("utf-8").replace(",&nbsp;","")
		avgs = getAvgs.findall(tr)
		stats = {
			"interest": float(avgs[0].decode("utf-8")),
			"knowledge": float(avgs[1].decode("utf-8")),
			"help": float(avgs[2].decode("utf-8")),
			"rating": float(avgs[3].decode("utf-8"))
		}
		inst.append({
			"id": id,
			"name": name,
			"position": position,
			"stats": stats
		})
	return inst


def getLink(link):
	global ret
	global num
	global count


	grid = None
	tables = None
	summary = None
	title = None

	text = subprocess.Popen(['wget','--load-cookies=cookies.txt', '-O', '-', link], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
	try:
		text = clean(text)
		title = parseTitle(getTitle.findall(text))
		try:
			summary = parseSummary(getSummary.findall(text))
		except:
			summary = None

		try:
			grid = parseInst(getGrid.findall(text))
		except:
			grid = None

		text = getMeans.sub(b"", text)
		text = getBars.sub(b"", text)

		try:
			tables = parseTables(getTables.findall(text))
		except:
			grid = None

		data = {
			"instructors": grid,
			"stats": tables,
			"summary": summary,
			"info": title
		}
		count = count + 1
		for id in title["ids"]:
			if (id in ret) == False:
				ret[id] = {}
			if (title["year"] in ret[id]) == False:
				ret[id][title["year"]] = {}
			ret[id][title["year"]][title["season"]] = data
		print(str(count) + "/" + str(num))
	except:
		title = None


def clean(text):
	#try:
	text = text.decode("utf-8")
	#except:
	#	print("ERROR!")
	#	print(text)
	text = "".join(text.split("\n"))
	text = "".join(text.split("\r"))
	text = "".join(text.split("\t"))
	text = text.strip()
	return text.encode("utf-8")

def saveChanges():
	with open('../static/storage/allEval.json', 'w') as outfile:
		json.dump(ret, outfile, indent=4, sort_keys=True)

with open('../static/storage/eval.json', 'r') as infile:
	with open('../static/storage/allEval.json','r') as infile2:
		if2 = infile2.read()
		if if2 == "":
			if2 = "{}"
		print(if2)
		ret = json.loads(if2)
		# stopped at 5000
		raw = infile
		data = json.load(raw)["data"]
		data = data[0:]
		num = len(data)
		for l in data:
			#l = data[0]
			link = start + l
			getLink(link)
			if count % 100 == 0:
				saveChanges()

'''
===========TITLE======================
get ids and titles from the header               <title>(.*?)</title>

===========table class="summary"=============
get # of people who could Respond
get # of people who did Respond 
get response rate
get overall rating (!!!)  


=========table .... class="grid"========                   
get instructors:
	get inistructor name
	get instructor role
	get instructor id
	get interest
	get knowledge
	get helped me learn
	get overall rating

=========table .... class="indivQuestions"======
[0]
subject expectations (avg, responses, median, std)
subjects learning objectives were met (....)
assignments contributed to my learning (....)
grading has been fair (....)

[1]
the pace of this class was (....)

[2]
of hours spent in classroom
of hours outside of classroom

[3]
overall rating (....)
'''