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
    url(r'^last_month_stats/$', views.last_month_stats, name='last_month_stats'),
    url(r'^get_datasources/$', views.get_datasources, name='get_datasources')
]