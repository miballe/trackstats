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

signer = Signer('secretKey')

# Hardcoded example
#	oauthAccessToken = "ya29.WgLhGc-UDgM73KWoWy6OBX0LjmpHYAWoWP7NrE573LpcPdAjnR3YGb-q5IjWWxOq7FUy"

# Converts time in milliseconds to nanoseconds
def timestamp_converter_nanos(date_time):
	timestamp_pattern = '%Y-%m-%dT%H:%M:%S.00Z'
	epoch = int(time.mktime(time.strptime(date_time, timestamp_pattern))) * 1000000000
	return epoch


# Returns average stats about last month for dashboard
def dashboard2(request):
	oauthAccessToken = signer.unsign(request.COOKIES.get("ACCESSTOKEN"))
	oauthAccessToken = "ya29.WgK0DSor04y7F7phLwE4DOzE_Pwmuvr_0sAnl9QXQcf0WQ7DG_PwU0YZCl7CQ9bNyppm"

	# Start-End times in timestamp format
	rawEndTime = datetime.datetime.now()
	endTime = rawEndTime.strftime('%Y-%m-%dT%H:%M:%S.00Z')
	startTime = (rawEndTime - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.00Z')

	# Start-End times in epoch nanoseconds time format
	endTimeNanos = timestamp_converter_nanos(endTime)
	startTimeNanos = timestamp_converter_nanos(startTime)

	# Get summary data about last month for dashboard
	weight = get_weight(oauthAccessToken, startTimeNanos, endTimeNanos)
	calories = get_total_calories(oauthAccessToken ,startTimeNanos, endTimeNanos)
	distance = get_total_distance(oauthAccessToken, startTimeNanos, endTimeNanos)
	nSessions = get_sessions_number(oauthAccessToken,startTime,endTime)

	dashboardSummary = str({'calories': str(round(calories,2)), 'distance': str(round(distance,2)), 'nsessions': str(nSessions), 'weight': str(weight)})

	return HttpResponse(dashboardSummary)	

# This function returns all sessions for a given time interval
# @request
# @sTime,eTime - strings from timestamps (in proper format!)
def get_sessions(token,sTime,eTime):

	session_params  = {'startTime':sTime , 'endTime': eTime , 'access_token' : token  }

	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = session_params )
	data = r.json()

	# testing json handling
	sessions = data["session"]

	return sessions


# This function returns the number of sessions for a given time interval.
# @request
# @sTime,eTime - strings from timestamps (in proper format!)
def get_sessions_number(token,sTime,eTime):

	session_params  = {'startTime':sTime , 'endTime': eTime , 'access_token' : token  }

	get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(get_sessions_url, params = session_params )
	data = r.json()

	sessions = data["session"]

	# sessions Number - to be displayed on dashboard !!
	sessionsNumber = len(sessions)

	return sessionsNumber



# Function that returns the last weight value or a string that promts user to submit weight.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
def get_weight(token,startTimeNanos,endTimeNanos):

	session_params  = {'access_token' : token  }

	last_weight_dataSourceId = "derived:com.google.weight:com.google.android.gms:merge_weight"
	last_weight_datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)
	weightOptions = {'userId': 'me' , 'dataSourceId': last_weight_dataSourceId , 'datasetId': last_weight_datasetId }

	last_weight_url = "https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}".format(**weightOptions)
	r = requests.get(last_weight_url, params = session_params )

	weightData = r.json()["point"]
	weight = "Submit Weight!"

	for it in weightData:
		weight = it["value"][0]["fpVal"]

	return weight


# Function that returns total calories on a given time interval - incomplete.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
def get_total_calories(token,startTimeNanos,endTimeNanos):

	session_params  = {'access_token' : token  }

	# Set parameters for request
	lastmonth_datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)

	# Last month calories summary request
	lastmonth_calories_dataSourceId = "derived:com.google.calories.expended:com.google.android.gms:from_activities"
	caloriesOptions = {'userId': 'me' , 'dataSourceId': lastmonth_calories_dataSourceId , 'datasetId': lastmonth_datasetId }
	lastmonth_calories_url = "https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}".format(**caloriesOptions)

	r = requests.get(lastmonth_calories_url, params = session_params )

	caloriesData = r.json()["point"]
	totalCalories = 0
	
	for it in caloriesData:
		totalCalories += it["value"][0]["fpVal"]

	return totalCalories


# Function that returns total calories on a given time interval - incomplete.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
def get_total_distance(token,startTimeNanos,endTimeNanos):

	session_params  = {'access_token' : token  }

	# Set parameters for request
	lastmonth_datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)

	# Last month calories summary request
	lastmonth_distance_dataSourceId = "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta"
	distanceOptions = {'userId': 'me' , 'dataSourceId': lastmonth_distance_dataSourceId , 'datasetId': lastmonth_datasetId }
	lastmonth_distance_url = "https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}".format(**distanceOptions)

	r = requests.get(lastmonth_distance_url, params = session_params )
	data = r.json()["point"]

	totalDistance = 0
	for it in data:
		totalDistance += it["value"][0]["fpVal"]

	return totalDistance

# Testing code
def select_session(request):

	dataSourceId = ""
	# The ID is formatted like: "startTime-endTime" where startTime and endTime are
	# 64 bit integers (epoch time with nanoseconds).
	datasetId = "1397513334728708316-2397515179728708316"
		
	select_session_url = "https://www.googleapis.com/fitness/v1/users/me/dataSources/"+ dataSourceId + "/datasets/" + datasetId + "?access_token=" + oauthAccessToken
	r = requests.get(select_session_url)

	print(r.status_code)
	data = r.json()

	return HttpResponse(str(data))

def sessions(request):
    return HttpResponse("[{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45}, {session: t3us76wk, date: 2015-12-05, calories: 423, distancekm: 5.9, avgspdkmh: 9.5, durationmins: 47}]")

def sessiondetails(request):
    return HttpResponse("{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45, starttime: '08:35:26', endtime: '09:20:47'}")

def get_datasources(request):
	return HttpResponse("make me!")
	
def dashboard(request):
    return HttpResponse("{'calories': 1234.56, 'distance': 34567.345, 'nsessions': 6, 'weight': 89.4}")