"""
Services
"""
from django.conf.urls import url

from . import views

app_name = 'services'
urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^workout/$', views.workout, name='workout')
    ]