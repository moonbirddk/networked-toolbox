"""
profiles urlconf

profiles:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^your-profile/$', views.profile, name='profile'),
]
