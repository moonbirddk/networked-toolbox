"""
tools urlconf

tools:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
