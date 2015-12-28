from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
import os
import ssl

import requests
from pprint import pprint


# Read credentials from json files 
credentials_dir = os.path.join(os.path.dirname(__file__), '../ClientIDSecret.json')

with open(credentials_dir, mode = 'r') as cred:
	data = json.load(cred)
	CLIENT_ID = data["web"]["client_id"]
	CLIENT_SECRET = data["web"]["client_secret"]

# pprint(str(CLIENT_ID))
# pprint(str(CLIENT_SECRET))

# Google Fit Scopes
ACT_READ = "https://www.googleapis.com/auth/fitness.activity.read"
LOC_READ = "https://www.googleapis.com/auth/fitness.location.read"
BODY_READ = "https://www.googleapis.com/auth/fitness.body.read"

#Example
# https://www.googleapis.com/fitness/v1/users/me/sessions?startTime=2014-04-01T00:00:00.00Z&endTime=2014-04-30T23:59:59.99Z
# Get current date
# END_TIME = "2016-04-01T00:00:00.00Z"
# Check if needed to add milliseconds
startTime = "2011-04-01T00:00:00.00Z" 
endTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.00Z')
# print END_TIME
oauthToken = "ya29.WAKqHmPicG8TLcFtxVUAEudPcIfOAwzxIbEr3USlziV-qhXL5c-8u9ZDotRNjmnYdK37"


def test_sessions(request):
	params = {'startTime':startTime , 'endTime': endTime , 'access_token' : oauthToken  }

	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = params )
	# print(r.status_code)
	data = r.json()
	#data = json.loads(r)
	return HttpResponse(str(data))

def select_session(request):
	# select_session_url = ""
	# r1 = requests.get()
	return HttpResponse("Expected to return a particular session")


def sessions(request):
    return HttpResponse("[{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45}, {session: t3us76wk, date: 2015-12-05, calories: 423, distancekm: 5.9, avgspdkmh: 9.5, durationmins: 47}]")

def sessiondetails(request):
    return HttpResponse("{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45, starttime: '08:35:26', endtime: '09:20:47'}")

