from django.shortcuts import render

# Create your views here.

def welcome(request):
    return render(request, 'frontend/welcome.html')

def dashboard(request):
    return render(request, 'frontend/dashboard.html')