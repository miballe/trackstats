from django.shortcuts import render
from django.core.signing import Signer
from django.core import signing
import logging
from httplib2 import Http
import json



# Create your views here.

def welcome(request):
    return render(request, 'frontend/welcome.html')

def dashboard(request):
    parser = Http()
    signer = Signer('secretKey')
    if request.COOKIES.get("ACCESSTOKEN"):
        accesstoken = signer.unsign(request.COOKIES.get("ACCESSTOKEN"))

    logging.info('DECRYPTED TOKEN - ' + accesstoken)

    resp, content = parser.request("https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(accessToken= accesstoken))

    user = json.loads(content)

    return render(request, 'frontend/newdash.html',{"username": user["name"],"userimg": user["picture"]})