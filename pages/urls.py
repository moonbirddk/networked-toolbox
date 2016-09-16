from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^pages/add(\d+)/$', views.add_page, name='add_page'),
    url(r'^([-\w]+)/$', views.show_page, name='show_page'),
]
