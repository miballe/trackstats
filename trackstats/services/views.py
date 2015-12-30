from django.shortcuts import render
from django.http import HttpResponse
import datetime
from datetime import date, timedelta
import time
import json
import os
from django.core.signing import Signer
import ssl
import logging

import requests
from pprint import pprint


EPOCH_START = datetime.datetime.utcfromtimestamp(0)

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


signer = Signer('secretKey')

# Hardcoded example
#	oauthAccessToken = "ya29.WgLhGc-UDgM73KWoWy6OBX0LjmpHYAWoWP7NrE573LpcPdAjnR3YGb-q5IjWWxOq7FUy"

# Converts time in milliseconds to nanoseconds
def timestamp_converter_nanos(date_time):
	timestamp_pattern = '%Y-%m-%dT%H:%M:%S.00Z'
	epoch = int(time.mktime(time.strptime(date_time, timestamp_pattern))) * 1000000000
	return epoch


# Returns average stats about last month for dashboard
def dashboard(request):
	oauthAccessToken = signer.unsign(request.COOKIES.get["ACCESSTOKEN"])

	rawEndTime = datetime.datetime.now()
	endTime = rawEndTime.strftime('%Y-%m-%dT%H:%M:%S.00Z')
	startTime = (rawEndTime - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.00Z')

	endTimeNanos = timestamp_converter_nanos(endTime)
	startTimeNanos = timestamp_converter_nanos(startTime)

	# Set parameters for request
	# params = {'startTime':startTime , 'endTime': endTime , 'access_token' : oauthAccessToken  }
	params = {'access_token' : oauthAccessToken  }
	lastmonth_datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)

	# Last month calories summary request
	lastmonth_calories_dataSourceId = "derived:com.google.calories.bmr:com.google.android.gms:merged"
	caloriesOptions = {'userId': 'me' , 'dataSourceId': lastmonth_calories_dataSourceId , 'datasetId': lastmonth_datasetId }
	lastmonth_calories_summary_url = "https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}".format(**caloriesOptions)
	rCalories = requests.get(lastmonth_calories_summary_url, params = params )
	# This variable should be handled to access last month calories data
	caloriesData = rCalories.json()


	# lastMonthSessions = get_sessions(request, startTime, endTime)
	lastMonthSessions = get_total_distance(request, startTimeNanos, endTimeNanos)

	return HttpResponse(lastMonthSessions)
	#return HttpResponse(str(caloriesData))
	# return HttpResponse(startTime + '---' + endTime)
	#return HttpResponse(get_summary_url)
	#return HttpResponse(lastmonth_datasetId)


# This function returns all sessions for a given time interval
# @request
# @sTime,eTime - strings from timestamps (in proper format!)
def get_sessions(request,sTime,eTime):

	oauthAccessToken = signer.unsign(request.COOKIES.get["ACCESSTOKEN"])

	startTime = sTime
	endTime = eTime
	session_params  = {'startTime':startTime , 'endTime': endTime , 'access_token' : oauthAccessToken  }

	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = session_params )
	# print(r.status_code)
	data = r.json()

	# testing json handling
	sessions = data["session"]

	# (ses[0]['activityType'])
	return sessions


# This function returns the number of sessions for a given time interval.
# @request
# @sTime,eTime - strings from timestamps (in proper format!)
def get_sessions_number(request,sTime,eTime):

	oauthAccessToken = signer.unsign(request.COOKIES.get["ACCESSTOKEN"])

	startTime = sTime
	endTime = eTime
	session_params  = {'startTime':startTime , 'endTime': endTime , 'access_token' : oauthAccessToken  }

	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = session_params )
	# print(r.status_code)
	data = r.json()

	# testing json handling
	sessions = data["session"]

	# sessions Number - to be displayed on dashboard !!
	sessionsNumber = len(sessions)

	return sessionsNumber


# Function that returns the last weight value or a string that promts user to submit weight.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
def get_weight(request,startTimeNanos,endTimeNanos):

	oauthAccessToken = signer.unsign(request.COOKIES.get["ACCESSTOKEN"])

	session_params  = {'access_token' : oauthAccessToken  }

	get_url1 = "https://www.googleapis.com/fitness/v1/users/me/"
	get_url2 = "dataSources/derived:com.google.weight:com.google.android.gms:merge_weight/"
	get_url3 = "datasets/" + str(startTimeNanos) + "-" + str(endTimeNanos)
	get_url_all = get_url1 + get_url2 + get_url3

	r = requests.get(get_url_all, params = session_params )

	weightdata = r.json()["point"]
	iter = len(weightdata)
	weight = "Submit Weight!"
	for it in weightdata:
		weight = it["value"][0]["fpVal"]

	return weight


# Function that returns total calories on a given time interval - incomplete.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
def get_total_calories(request,startTimeNanos,endTimeNanos):

	oauthAccessToken = signer.unsign(request.COOKIES.get["ACCESSTOKEN"])

	session_params  = {'access_token' : oauthAccessToken  }

	get_url1 = "https://www.googleapis.com/fitness/v1/users/me/"
	get_url2 = "dataSources/derived:com.google.calories.expended:com.google.android.gms:from_activities/"
	get_url3 = "datasets/" + str(startTimeNanos) + "-" + str(endTimeNanos)
	get_url_all = get_url1 + get_url2 + get_url3

	r = requests.get(get_url_all, params = session_params )

	caloriesdata = r.json()["point"]

	totalcalories = 0
	for it in caloriesdata:
		totalcalories += it["value"][0]["fpVal"]

	return totalcalories


# Function that returns total calories on a given time interval - incomplete.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
def get_total_distance(request,startTimeNanos,endTimeNanos):

	oauthAccessToken = signer.unsign(request.COOKIES.get["ACCESSTOKEN"])

	session_params  = {'access_token' : oauthAccessToken  }

	get_url1 = "https://www.googleapis.com/fitness/v1/users/me/"
	get_url2 = "dataSources/derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta/"
	get_url3 = "datasets/" + str(startTimeNanos) + "-" + str(endTimeNanos)
	get_url_all = get_url1 + get_url2 + get_url3

	r = requests.get(get_url_all, params = session_params )

	data = r.json()["point"]

	totaldistance = 0
	for it in data:
		totaldistance += it["value"][0]["fpVal"]

	return totaldistance



# Returns a list of all sessions of the user starting from the beginning of timestamps until today
def all_sessions(request):

	oauthAccessToken = signer.unsign(request.COOKIES.get["ACCESSTOKEN"])

	startTime = EPOCH_START
	endTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.00Z')

	params = {'startTime':startTime , 'endTime': endTime , 'access_token' : oauthAccessToken  }

	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = params )
	# print(r.status_code)
	data = r.json()

	return HttpResponse(str(data))


# Testing code
def select_session(request):
	# select_session_url = ""
	# r1 = requests.get()
	dataSourceId = ""
	# The ID is formatted like: "startTime-endTime" where startTime and endTime are
	# 64 bit integers (epoch time with nanoseconds).
	datasetId = "1397513334728708316-2397515179728708316"
		
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

def get_datasources(request):
	return HttpResponse("make me!")