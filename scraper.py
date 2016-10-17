import urllib.request
import uuid
import re

# uuid.uuid1()
all_subjs = urllib.request.urlopen("http://catalog.mit.edu/subjects/").read()

pattern = re.compile(b'<a href="\/subjects\/(.*?)\/">(.*?)<\/a>', re.IGNORECASE)
match = pattern.findall(all_subjs)

subj_info = []
for m in match:
	name = m[1].decode("utf-8")
	id = m[0].decode("utf-8")
	subj_info.append([id,name])

print(subj_info)