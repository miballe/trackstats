"""
Services
"""
from django.conf.urls import url

from . import views

app_name = 'services'
urlpatterns = [
    url(r'^sessions/$', views.sessions, name='sessions'),
    url(r'^sessiondetails/$', views.sessiondetails, name='sessiondetails'),
    url(r'^test_sessions/$', views.test_sessions, name='test_sessions'),
    url(r'^select_session/$', views.select_session, name='select_session')

]