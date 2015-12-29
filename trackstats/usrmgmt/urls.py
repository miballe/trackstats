"""
UsrMgmt URLs file
"""
from django.conf.urls import url

from . import views

app_name = 'usrmgmt'
urlpatterns = [
    url(r'^login/$', views.login, name='auth'),
    url(r'^loginac/$', views.auth, name='auth'),
    url(r'^logout/$', views.logout, {'next_page': '/',}, name='logout'),
]