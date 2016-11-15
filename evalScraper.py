import urllib.request
import uuid
import re
import json

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()

url1 = "https://edu-apps.mit.edu/ose-rpt/subjectEvaluationReport.htm?surveyId=586&subjectGroupId=39DA981926B31A2BE0533D2F09127E7F&subjectId=2.821"
# step 1: export chrome cookies to cookies.txt