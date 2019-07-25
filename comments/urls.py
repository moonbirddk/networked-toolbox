from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add-comment/', views.add, name="add"),
    path('like_comment/(\d+)/', views.like_comment, name='like'), 
    path('unlike_comment/(\d+)/', views.unlike_comment, name='unlike'), 
]
