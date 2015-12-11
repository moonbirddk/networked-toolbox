"""
tools urlconf

tools:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/([a-z]+)/(\d+)/$', views.add, name='add'),
    url(r'^(\d+)/delete/$', views.delete, name='delete'),
]
