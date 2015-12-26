"""
Services
"""
from django.conf.urls import url

from . import views

app_name = 'services'
urlpatterns = [
    url(r'^sessions/$', views.sessions, name='sessions'),
    url(r'^sessiondetails/$', views.sessiondetails, name='sessiondetails'),
]