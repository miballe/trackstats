# from django.shortcuts import render
# from django.http import HttpResponse
import datetime
import json
import os

# import httplib2
# import urllib2
# from googleapiclient.discovery import build
# from oauth2client.client import OAuth2WebServerFlow
# import requests
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


START_TIME = "2011-04-01T00:00:00.00Z" 
# Get current date
#END_TIME = "2016-04-01T00:00:00.00Z"
# Check if needed to add milliseconds
END_TIME = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.00Z')
# print END_TIME

#https://www.googleapis.com/fitness/v1/users/me/sessions?startTime=2014-04-01T00:00:00.00Z&endTime=2014-04-30T23:59:59.99Z
#RESOURCE_PATH = "/users/me/sessions?"
OAUTH_TOKEN = "ya29.WAIGNOCSCTkj0vy3DJxCpOwsuek2KK8ujbz1ENrYyKWrEuMv-bCAJrb35ApdoOBqIu5Q"

get_sessions_url = "https://www.googleapis.com/fitness/v1/users/me/sessions?startTime=" + START_TIME + "&endTime=" + END_TIME + "&access_token=" + OAUTH_TOKEN

#r = requests.get(get_sessions_url)
#print(r.status_code)
#print(get_sessions_url)

#data = r.json()
#print data
# data = json.loads(r)
# print(data)



def sessions(request):
    return HttpResponse("[{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45}, {session: t3us76wk, date: 2015-12-05, calories: 423, distancekm: 5.9, avgspdkmh: 9.5, durationmins: 47}]")

def sessiondetails(request):
    return HttpResponse("{sessionid: 'r38w29jk', date: '2015-12-04', calories: 348, distancekm: 4.8, avgspdkmh: 8.7, durationmins: 45, starttime: '08:35:26', endtime: '09:20:47'}")

