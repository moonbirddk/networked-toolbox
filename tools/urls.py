"""
tools urlconf

tools:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
   # url(r'^$', views.index, name='index'),
    url(r'^$', views.list_categories, name='index'),
    url(r'^tools/$', views.list_tools, name='list_tools'), 
    url(r'^tools/(\d+)/$', views.show_tool, name='show'),
    
    url(r'^tools/add/$', views.add_tool, name='add'),
    url(r'^tools/edit/(\d+)/$', views.edit_tool, name='edit'),
    url(r'^tools/follow/(\d+)/$', views.follow_tool, name='follow'),
    url(r'^tools/unfollow/(\d+)/$', views.unfollow_tool, name='unfollow'),
    url(r'^story/add/tool/(\d+)/$', views.add_story, name='add_story'),
    url(r'^story/add/workarea/(\d+)/$', views.add_workarea_story, name='add_workarea_story'),
    url(r'^story/(\d+)/$', views.show_story, name='show_story'),
    url(r'^toolboxes/add/$', views.add_category, name='add_category'),
    url(r'^(\d+)/toolboxes/add/$', views.add_category, name='add_category_to_group'), 
    url(r'^toolboxes/show/(\d+)/$', views.show_category, name='show_category'),
    url(r'^toolboxes/edit/(\d+)/$', views.edit_category, name='edit_category'),
    url(r'^toolboxes/delete/(\d+)/$', views.delete_category, name='delete_category'),

    url(r'^add/$', views.add_categorygroup, name='add_categorygroup'),
    url(r'^edit/(\d+)/$', views.edit_categorygroup, name='edit_categorygroup'),
    url(r'^delete/(\d+)/$', views.delete_categorygroup, name='delete_categorygroup'),
    url(r'^show/(\d+)/$', views.show_categorygroup, name='show_categorygroup'),
    url(r'^suggestion/([a-z]+)/(\d+)/$', views.add_suggestion, name='add_suggestion'),

    url(r'^overview/edit/([a-z]+)/$', views.edit_overview, name='edit_overview'),
]
