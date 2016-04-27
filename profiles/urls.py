"""
profiles urlconf

profiles:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^terms-and-conditions$', views.terms_and_conditions,
        name='terms_and_conditions'),
    url(r'^([\da-zA-Z]{32})/$', views.show, name='show'),
    url(r'^([\da-zA-Z]{32})/tools$', views.show_tools, name='show_tools'),
    url(r'^edit$', views.edit, name='edit'),
]
