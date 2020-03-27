from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add-comment/', views.add, name="add"),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like'), 
    path('unlike_comment/<int:comment_id>/', views.unlike_comment, name='unlike'), 
]
