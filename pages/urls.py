from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.add_page, name='add_page'),
    url(r'^([-\w]+)/edit/$', views.edit_page, name='edit_page'),
    url(r'^([-\w]+)/$', views.show_page, name='show_page'),
]
