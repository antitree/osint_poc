#!/usr/bin/python

import requests
import sys
import os
import numpy
#import matplotlib.pyplot as plt
import datetime
import sqlite3

from collections import OrderedDict
from graphy.backends import google_chart_api

import webbrowser
 
user = sys.argv[1]
 
r = requests.get('http://www.reddit.com/user/' + user + '.json')
j = r.json()
posts = [x for x in j['data']['children']]
#collect graph data
d = [q["data"]["created"] for q in posts]
types = [r["kind"] for r in posts]
 
dates = [datetime.datetime.fromtimestamp(d) for d in d]

#plot days of the week
days = [datetime.date.weekday(x) for x in dates]
daycount = OrderedDict([('Monday',0), ('Tuesday',0), ('Wednesday',0), ('Thursday',0), ('Friday',0),
						('Saturday',0), ('Sunday',0)])

for x in days:
	if x is 0:
		daycount["Monday"] += 1
	elif x is 1:
		daycount["Tuesday"] += 1
	elif x is 2:
		daycount["Wednesday"] += 1
	elif x is 3:
		daycount["Thursday"] += 1
	elif x is 4:
		daycount["Friday"] += 1
	elif x is 5:
		daycount["Saturday"] += 1
	elif x is 6:
		daycount["Sunday"] += 1
					
day_chart = google_chart_api.LineChart(daycount.values())
day_chart.bottom.labels = daycount.keys()
day_url = day_chart.display.Url(400,100)
print "\nLink to graph of Activity Per Day:"
print day_url

try:
  webbrowser.open_new(day_url)
except:
  print("Couldn't open browser")
 
#plat time of the day
hours = [y.hour for y in dates]
hourcount = OrderedDict()
for x in range(0,24):
	hourcount[str(x)] = 0
	
for x in hours:
	hourcount[str(x)] += 1

hour_chart = google_chart_api.LineChart(hourcount.values())
hour_chart.bottom.labels = hourcount.keys()
print ""
hour_url = hour_chart.display.Url(400,100)
print "Link to graph of Activity per Hour:"
print hour_url
print ""

try:
  webbrowser.open_new_tab(hour_url)
except:
  print("couldn't open browser")

charts = [day_url, hour_url]

#add findings to database
if not os.path.isfile('%s.db' % sys.argv[1]):
	conn = sqlite3.connect('%s.db' % sys.argv[1])
	c = conn.cursor()

	c.execute('''CREATE TABLE daycount (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)''')
	c.execute('''CREATE TABLE hourcount ('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23')''')
	c.execute('''CREATE TABLE chartlinks (Days, Hours)''')
else:
	conn = sqlite3.connect('%s.db' % sys.argv[1])
	c = conn.cursor()	
	
c.execute('INSERT INTO daycount VALUES(?, ?, ?, ?, ?, ?, ?)', daycount.values())
c.execute('''INSERT INTO hourcount VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', hourcount.values())
c.execute('''INSERT INTO chartlinks VALUES (?, ?)''', charts)

conn.commit()
conn.close()
