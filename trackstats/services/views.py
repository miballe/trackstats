from django.shortcuts import render
from django.http import HttpResponse
import datetime
from datetime import date, timedelta
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
# print END_TIME
oauthAccessToken = "ya29.WQKcvdSCoDyRPb5lztUHl_6QTLiopU8Qv-8349ASSi_O95iuoo_rAOzlaTwVARDsI2ir"


def last_month_stats(request):


	rawEndTime = datetime.datetime.now()
	endTime = rawEndTime.strftime('%Y-%m-%dT%H:%M:%S.00Z')
	startTime = (rawEndTime - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.00Z')
	
	# Set parameters for request
	params = {'startTime':startTime , 'endTime': endTime , 'access_token' : oauthAccessToken  }


	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = params )
	data = r.json()
	
	return HttpResponse(str(data))
	#return HttpResponse(startTime + '---' + endTime)


def all_sessions(request):

	startTime = "1970-01-01T00:00:00.00Z" 
	endTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.00Z')
	params = {'startTime':startTime , 'endTime': endTime , 'access_token' : oauthAccessToken  }

	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = params )
	# print(r.status_code)
	data = r.json()
	#data = json.loads(r)

	return HttpResponse(str(data))

def select_session(request):
	# select_session_url = ""
	# r1 = requests.get()
	dataSourceId = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
	# The ID is formatted like: "startTime-endTime" where startTime and endTime are
	# 64 bit integers (epoch time with nanoseconds).
	#datasetId = "1448983095955-144898712705"
	datasetId = "1397513334728708316-2397515179728708316"
	#DATA_SET  = "1051700038292387000-1451700038292387000"
	

	# select_session_url = "https://www.googleapis.com/fitness/v1/users/me/dataSources/dataSourceId/datasets/datasetId"
	#https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:com.google.android.gms:estimated_steps/datasets/1397513334728708316-2397515179728708316?access_token=ya29.WQLcdzzGy0WQ5KvEP7RABSi4audkXnY1m-IIiYR94Ac6vxL5T8eBIANLdu99anPJBdlB
	select_session_url = "https://www.googleapis.com/fitness/v1/users/me/dataSources/"+ dataSourceId + "/datasets/" + datasetId + "?access_token=" + oauthAccessToken
	r = requests.get(select_session_url)

	print(r.status_code)
	data = r.json()


	#return HttpResponse("Expected to return a particular session")
	return HttpResponse(str(data))

def sessions(request):
    return HttpResponse("[{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45}, {session: t3us76wk, date: 2015-12-05, calories: 423, distancekm: 5.9, avgspdkmh: 9.5, durationmins: 47}]")

def sessiondetails(request):
    return HttpResponse("{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45, starttime: '08:35:26', endtime: '09:20:47'}")

