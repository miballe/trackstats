"""
UsrMgmt URLs file
"""
from django.conf.urls import url

from . import views

app_name = 'usrmgmt'
urlpatterns = [
    url(r'^login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^logindone/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
]