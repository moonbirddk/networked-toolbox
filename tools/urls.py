"""
tools urlconf

tools:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
   # url(r'^$', views.index, name='index'),
    url(r'^$', views.list_category_groups, name='index'),
    url(r'^tools/$', views.list_tools, name='list_tools'), 
    url(r'^tools/(\d+)/$', views.show_tool, name='show'),
    url(r'^tools/follow/(\d+)/$', views.follow_tool, name='follow'),
    url(r'^tools/unfollow/(\d+)/$', views.unfollow_tool, name='unfollow'),
    url(r'^follow/(\d+)/$', views.follow_category_group, name='follow_work_area'),
    url(r'^unfollow/(\d+)/$', views.unfollow_category_group, name='unfollow_work_area'),
    url(r'^stories/story/add/tool/(\d+)/$', views.add_story, name='add_story'),
    url(r'^stories/story/add/workarea/(\d+)/$', views.add_workarea_story, name='add_workarea_story'),
    url(r'^stories/$', views.show_all_stories, name='show_all_stories'), 
    url(r'^stories/story/(\d+)/$', views.show_story, name='show_story'),
    url(r'^stories/story/edit/(\d+)/$', views.edit_story, name='edit_story'),
    url(r'^toolboxes/show/(\d+)/$', views.show_category, name='show_category'),
     url(r'^show/(\d+)/$', views.show_categorygroup, name='show_categorygroup'),
    url(r'^suggestion/([a-z]+)/(\d+)/$', views.add_suggestion, name='add_suggestion'),
    url(r'^overview/edit/([a-z]+)/$', views.edit_overview, name='edit_overview'),
]
