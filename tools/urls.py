"""
tools urlconf

tools:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/(\d+)/$', views.edit, name='edit'),
    url(r'^(\d+)/$', views.show, name='show'),

    url(r'^(\d+)/resources/add/$', views.add_resource, name='add_resource'),
    url(r'^(\d+)/resources/(\d+)/delete/$', views.delete_resource, name='delete_resource'),

]
