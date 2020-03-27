"""
events urlconf

events_workshops:url_name
"""

from django.urls import path

from .views import list_events, show_event, event_signup, event_signoff
app_name = 'events_workshops'
urlpatterns = [
   # url(r'^', views.index, name='index'),
    path('', list_events, name='list_events'), 
    path('<int:id>/', show_event, name='show_event'),
    path('<int:id>/signup_user/', event_signup, name='signup_event'),
    path('<int:id>/signoff_user/', event_signoff, name='signoff_event'),
    #path('signoff_user/', show_event, name='show_event'),
    
]
