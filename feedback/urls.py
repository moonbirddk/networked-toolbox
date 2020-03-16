from django.conf.urls import include, url
from django.urls import path


from .views import send_feedback

app_name = 'feedback'

urlpatterns = [
    path('send/', send_feedback, name="send_feedback"),
     
]
