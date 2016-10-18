import urllib.request
import uuid
import re
import json

# uuid.uuid1()
all_subjs = urllib.request.urlopen("http://catalog.mit.edu/subjects/").read()

pattern = re.compile(b'<a href="\/subjects\/(.*?)\/">(.*?)<\/a>', re.IGNORECASE)
pattern2 = re.compile(b'<div class="courseblock">(.*?)<strong>(.*?)<\/strong>(.*?)<p class="courseblockdesc">(.*?)<\/p>(.*?)<\/div>', re.S)
pattern3 = re.compile(b'<(.*?)>', re.S)
match = pattern.findall(all_subjs)

subj_info = []
for m in match:
	name = m[1].decode("utf-8")
	id = m[0].decode("utf-8")
	subj_info.append([id,name])

subj_data = []

for i in range(0,len(subj_info)): # len(subj_info)
	print("starting parsing course:",subj_info[i][0])
	subj = subj_info[i]
	subj_file = urllib.request.urlopen("http://catalog.mit.edu/subjects/" + subj[0]).read()
	match = pattern2.findall(subj_file)

	"""
	0: html text (useless)
	1: title of class and id (useful)
	2: prereq info and other stuff
	3: desc
	4: instructor

	"""
	for j in range(0,len(match)): # len(match)
		block = match[j]

		title_and_id = block[1].decode("utf-8").split(" ")
		id = title_and_id[0]
		title = " ".join(title_and_id[1::])
		desc_unparsed = block[3] # need to remove links...
		desc = pattern3.sub(b"", desc_unparsed).decode("utf-8")
		desc = " ".join(desc.split("\n")).strip()

		subj_data.append({
			"id": id,
			"title": title,
			"desc": desc
		})

save_data = {
	"courses": subj_data
}

# save path is storage/classes.json
with open('storage/classes.json', 'w') as outfile:
    json.dump(save_data, outfile, indent=4, sort_keys=True)