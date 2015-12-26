"""
Pages
"""
from django.conf.urls import url

from . import views

app_name = 'frontend'
urlpatterns = [
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]