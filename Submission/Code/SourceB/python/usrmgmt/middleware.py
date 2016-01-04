import logging
import urllib
from django.http import HttpResponseRedirect
from google.appengine.api import users
from httplib2 import Http
from django.core.signing import Signer

ACT_READ = "https://www.googleapis.com/auth/fitness.activity.read"
LOC_READ = "https://www.googleapis.com/auth/fitness.location.read"
BODY_READ = "https://www.googleapis.com/auth/fitness.body.read"
#this file applies loginMiddleware function for each request
class loginMiddleware(object):

    def process_request(self,request):
        parser = Http()
        scope = ACT_READ+' '+LOC_READ+' '+BODY_READ
        user = users.get_current_user()
        DESTINATION = str(request.path)
        ACCESSTOKEN = request.COOKIES.get('ACCESSTOKEN')
        signer = Signer('secretKey')
        if ACCESSTOKEN :
            ACCESSTOKEN = signer.unsign(ACCESSTOKEN)
        #checks the login status for each request
        resp, content = parser.request("https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(accessToken= ACCESSTOKEN))


        logging.info(resp.status)
        #except the following urls
        if DESTINATION != '/' and '/pages/welcome/' not in DESTINATION and '/usr/login/' not in DESTINATION and '/usr/loginac/' not in DESTINATION:
            if resp.status != 200:
                logging.info('redirection needed  ' + DESTINATION)
                return HttpResponseRedirect('/?redirect=' + DESTINATION)