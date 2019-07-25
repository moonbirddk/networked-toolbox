"""
profiles urlconf

profiles:url_name
"""

from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('terms-and-conditions', views.terms_and_conditions,
        name='terms_and_conditions'),
    path('<uuid>/', views.show, name='show'),
    path('([\da-zA-Z]{32})/tools', views.show_tools, name='show_tools'),
    path('edit', views.edit, name='edit'),
    path('resend-verification',
        views.resend_verification,
        name='resend_verification'),
]
