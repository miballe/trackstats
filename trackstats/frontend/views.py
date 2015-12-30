from django.shortcuts import render
from django.core.signing import Signer
from django.core import signing
import logging



# Create your views here.

def welcome(request):
    return render(request, 'frontend/welcome.html')

def dashboard(request):
    signer = Signer('secretKey')
    accesstoken = signer.unsign(request.COOKIES["ACCESSTOKEN"])
    logging.info('DECRYPTED TOKEN - ' + accesstoken)
    return render(request, 'frontend/dashboard.html')