from django.conf.urls import url

from . import views

urlpatterns = [
  
    url(r'^([-\w]+)/$', views.show_page, name='show_page'),
]
