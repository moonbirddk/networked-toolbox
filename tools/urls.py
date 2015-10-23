"""
tools urlconf

tools:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.add_tool, name='add_tool'),
]
