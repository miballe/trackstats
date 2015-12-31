from __future__ import division
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


signer = Signer('secretKey')



# Converts time in milliseconds to nanoseconds
def timestamp_converter_nanos(date_time):
	timestamp_pattern = '%Y-%m-%dT%H:%M:%S.00Z'
	epoch = int(time.mktime(time.strptime(date_time, timestamp_pattern))) * 1000000000
	return epoch

# Converts time from milliseconds to nanoseconds	
def millis_converter_nanos(milliseconds):
	return milliseconds * 1000000

# Returns average stats about last month for dashboard
def dashboard(request):
	oauthAccessToken = signer.unsign(request.COOKIES.get("ACCESSTOKEN"))
	# oauthAccessToken = "ya29.WgK0DSor04y7F7phLwE4DOzE_Pwmuvr_0sAnl9QXQcf0WQ7DG_PwU0YZCl7CQ9bNyppm"

	# Start-End times in timestamp format
	rawEndTime = datetime.datetime.now()
	endTime = rawEndTime.strftime('%Y-%m-%dT%H:%M:%S.00Z')
	startTime = (rawEndTime - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.00Z')

	# Start-End times in epoch nanoseconds time format
	endTimeNanos = timestamp_converter_nanos(endTime)
	startTimeNanos = timestamp_converter_nanos(startTime)

	# Get summary data about last month for dashboard
	weight = get_weight(oauthAccessToken, startTimeNanos, endTimeNanos)
	calories = get_calories(oauthAccessToken ,startTimeNanos, endTimeNanos, False)
	distance = get_detailed_distance(oauthAccessToken, startTimeNanos, endTimeNanos, False)
	nSessions = get_sessions(oauthAccessToken,startTime,endTime, False)

	dashboardSummary = str({'calories': str(round(calories,2)), 'distance': str(round(distance,2)), 'nsessions': str(nSessions), 'weight': str(weight)})

	return HttpResponse(dashboardSummary)	

# This function returns all sessions for a given time interval
# @request
# @sTime,eTime - strings from timestamps (in proper format!)
# @boo : boolean parameter - True to return sessions dataset - False for total session number only
def get_sessions(token,sTime,eTime, boo):

	session_params  = {'startTime':sTime , 'endTime': eTime , 'access_token' : token  }

	url = "https://www.googleapis.com/fitness/v1/users/me/sessions"
	r = requests.get(url, params = session_params )
	data = r.json()

	sessions = data["session"]
	
	if boo is True:
		return [sessions, len(sessions)]
	else:
		return len(sessions)





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
# @boo : boolean parameter - True to return the dataset to be plotted - False for total calories only
def get_calories(token,startTimeNanos,endTimeNanos, boo):

	session_params  = {'access_token' : token  }

	# Set parameters for request
	datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)

	# Last month calories summary request
	dataSourceId = "derived:com.google.calories.expended:com.google.android.gms:from_activities"
	options = {'userId': 'me' , 'dataSourceId': dataSourceId , 'datasetId': datasetId }
	url = "https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}".format(**options)

	r = requests.get(url, params = session_params )

	
	data = r.json()["point"]
	totalCalories = 0
	
	for it in data:
		totalCalories += it["value"][0]["fpVal"]

	
	if boo is True:
		return [totalCalories, data]
	else:
		return totalCalories
	


	
# Function that returns distance data on a given time interval - incomplete.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
# @boo : boolean parameter - True to return the dataset to be plotted - False for total distance only
def get_detailed_distance(token,startTimeNanos,endTimeNanos, boo):

	session_params  = {'access_token' : token  }

	# Set parameters for request
	datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)

	# Last month calories summary request
	dataSourceId = "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta"
	options = {'userId': 'me' , 'dataSourceId': dataSourceId , 'datasetId': datasetId }
	url = "https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}".format(**options)

	r = requests.get(url, params = session_params )
	data = r.json()["point"]

	totalDistance = 0
	for it in data:
		totalDistance += it["value"][0]["fpVal"]
		# data to frontend documentation
		# data is a list of json objects
		# to access them use the following:
		# x = it["endTimeNanos"]
		# f(x) = it["value"][0]["fpVal"]

	if boo is True:
		return [totalDistance, data]
	else:
		return totalDistance
	

	
	

# Function that returns speed data on a given time interval - incomplete.
# @request
# @startTimeNanos,endTimeNanos - epoch time in nanoseconds
# @boo : boolean parameter - True to return the dataset to be plotted - False for average distance only
def get_detailed_speed(token,startTimeNanos,endTimeNanos, boo):

	session_params  = {'access_token' : token  }

	# Set parameters for request
	datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)

	# Last month calories summary request
	dataSourceId = "derived:com.google.speed:com.google.android.gms:merge_speed"
	options = {'userId': 'me' , 'dataSourceId': dataSourceId , 'datasetId': datasetId }
	url = "https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}".format(**options)

	if boo is True:
		r = requests.get(url, params = session_params )
		data = r.json()["point"]

	
	totalDistance = get_detailed_distance(token,startTimeNanos,endTimeNanos, False)
	timeInterval = (endTimeNanos - startTimeNanos)/1000000000
	avgspeed = totalDistance/timeInterval

	if boo is True:
		return [avgspeed, data]
	else:
		return avgspeed


# Function that gives the information required to create the session page for the user (plot_data and summary). 
# The query from front end should include starttime and endtime in milliseconds
# we will need to convert them in nanoseconds.
def get_session_details(request):

	oauthAccessToken = signer.unsign(request.COOKIES.get("ACCESSTOKEN"))
	# oauthAccessToken = "ya29.WgK0DSor04y7F7phLwE4DOzE_Pwmuvr_0sAnl9QXQcf0WQ7DG_PwU0YZCl7CQ9bNyppm"
	
	
	# hardcoded times - we need them from the front end from users choice !!!
	startTime = 1448983095955
	endTime = 1548987127050

	# Start-End times in epoch nanoseconds time format
	endTimeNanos = millis_converter_nanos(endTime)
	startTimeNanos = millis_converter_nanos(startTime)
	
	# datasetId = str(startTimeNanos) + "-" + str(endTimeNanos)
	
		
	# create deliverables
	# 0 item in list is total distance
	# 1 item in list is data dictionary
	speed = get_detailed_speed(oauthAccessToken, startTimeNanos, endTimeNanos, True)
	calories = get_calories(oauthAccessToken, startTimeNanos, endTimeNanos, True)
	
	average = str({'avgspeed': round(speed[0],4), 'totalcalories': round(calories[0],2)})
	data = str(list([speed[1], calories[1]]))
	
	return HttpResponse([average, data])
	
