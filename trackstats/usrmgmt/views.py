from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.core.signing import Signer
from django.core import signing
from httplib2 import Http
import urllib
import json
import os
import logging


credentials_dir = os.path.join(os.path.dirname(__file__), '../ClientIDSecret.json')
ACT_READ = "https://www.googleapis.com/auth/fitness.activity.read"
LOC_READ = "https://www.googleapis.com/auth/fitness.location.read"
BODY_READ = "https://www.googleapis.com/auth/fitness.body.read"
PROFILE = "https://www.googleapis.com/auth/userinfo.profile"
with open(credentials_dir, mode = 'r') as cred:
	data = json.load(cred)
	CLIENT_ID = data["web"]["client_id"]
	CLIENT_SECRET = data["web"]["client_secret"]

# Create your views here.
def login(request):
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = CLIENT_ID
    redirect_uri = "http://localhost:8080/usr/loginac/"
    scope = ACT_READ+' '+LOC_READ+' '+BODY_READ+' '+PROFILE
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
            token_request_uri=token_request_uri,
            response_type=response_type,
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope)

    response = HttpResponseRedirect(url)
    return response



def auth(request):

    parser = Http()
    login_failed_url = '/'
    authcode = request.GET['code']
    logging.info(authcode)
    if authcode:

        access_token_uri = "https://www.googleapis.com/oauth2/v4/token"

        params = urllib.urlencode({
            'code': authcode,
            'redirect_uri': "http://localhost:8080/usr/loginac/",
            'client_id': "1047651366452-32ph4ndul3s5caub46t3nbue3p5e5uha",
            'client_secret': "PNwEP-rCdeP8rBreZ8oWjUle",
            'grant_type': 'authorization_code'
        })

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        resp, content = parser.request(access_token_uri, method = 'POST', body = params, headers = headers)
        content = json.loads(content)
        tokendata = content['access_token']
        logging.info('ORIGINAL TOKEN - ' + tokendata)
        redirection = request.COOKIES.get('REDIRECTION')
        if redirection:
            response = HttpResponseRedirect(redirection)
            response.delete_cookie('REDIRECTION')
        else:
            response = HttpResponseRedirect('/pages/dashboard')

        signer = Signer('secretKey')
        encryptedToken = signer.sign(tokendata)
        logging.info('ENCRYPTED TOKEN - ' + encryptedToken)
        response.set_cookie("ACCESSTOKEN", encryptedToken, max_age=5000)

        return response

    else:
        return HttpResponseRedirect('/pages/welcome')

def logout(request):
    return HttpResponse("Signed out!")