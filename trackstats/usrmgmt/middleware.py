import logging
import urllib
from django.http import HttpResponseRedirect


class loginMiddleware(object):

    def process_request(self,request):
        DESTINATION = str(request.path)
        ACCESSTOKEN = request.COOKIES.get('ACCESSTOKEN')
        if DESTINATION != '/' and '/pages/welcome/' not in DESTINATION and '/usr/login/' not in DESTINATION and '/usr/loginac/' not in DESTINATION:
            if not ACCESSTOKEN:
                logging.info('redirection needed  ' + DESTINATION)
                return HttpResponseRedirect('/?redirect=' + DESTINATION)