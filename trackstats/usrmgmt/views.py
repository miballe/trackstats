from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def loginac(request):
    return HttpResponse("Reached the Authorization Code processing method")

def logout(request):
	return HttpResponse("Signed out!")