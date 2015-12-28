"""
UsrMgmt URLs file
"""
from django.conf.urls import url

from . import views

app_name = 'usrmgmt'
urlpatterns = [
    url(r'^loginac/$', views.loginac, name='loginac'),
    url(r'^logout/$', views.logout, {'next_page': '/',}, name='logout'),
]