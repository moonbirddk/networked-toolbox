from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add-comment/', views.add, name="add"),
    url(r'^like_comment/(\d+)/$', views.like_comment, name='like'), 
    url(r'^unlike_comment/(\d+)/$', views.unlike_comment, name='unlike'), 
]
