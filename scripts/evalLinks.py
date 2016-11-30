import re
import json
import subprocess

main_url = "https://edu-apps.mit.edu/ose-rpt/subjectEvaluationSearch.htm?termId=&departmentId=&subjectCode=*&instructorName=&search=Search"

# wget -O - http://www.somesite.org/
# wget --load-cookies=cookies.txt https://edu-apps.mit.edu/ose-rpt/subjectEvaluationSearch.htm\?termId\=2016SP\&departmentId\=\&subjectCode\=\*\&instructorName\=\&search\=Search


#
# GET MAIN
#

main_text = subprocess.Popen(['wget','--load-cookies=cookies.txt', '-O', '-', main_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

a_pattern = re.compile(b'<a href="(.*?)">(.*?)</a>', re.S)
# <div id="rh-col"> ... <div>
# find all <a ... </a> and discard the first one
a_s = a_pattern.findall(main_text[0])
links = {
	"data": []
}
for a in a_s:
	href = a[0].decode("utf-8")
	text = a[0].decode("utf-8")
	if "surveyId" in href:
		links["data"].append(href)

with open('../static/storage/evalLinkss.json', 'w') as outfile:
    json.dump(links, outfile, indent=4, sort_keys=True)