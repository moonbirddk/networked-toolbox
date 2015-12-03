"""
profiles urlconf

profiles:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^terms-and-conditions$', views.terms_and_conditions,
        name='terms_and_conditions'),
    url(r'^your-profile/$', views.profile, name='profile'),
]
