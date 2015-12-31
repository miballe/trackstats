"""
Services
"""
from django.conf.urls import url

from . import views

app_name = 'services'
urlpatterns = [
    url(r'^get_session_details/$', views.get_session_details, name='get_session_details'),
    url(r'^dashboard/$', views.dashboard, name='dashboard')
    ]