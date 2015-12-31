"""
Services
"""
from django.conf.urls import url

from . import views

app_name = 'services'
urlpatterns = [
    url(r'^sessions/$', views.sessions, name='sessions'),
    url(r'^sessiondetails/$', views.sessiondetails, name='sessiondetails'),
    url(r'^all_sessions/$', views.all_sessions, name='all_sessions'),
    url(r'^select_session/$', views.select_session, name='select_session'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^dashboard2/$', views.dashboard2, name='dashboard2')
    ]