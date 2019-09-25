"""
tools urlconf

tools:url_name
"""

from django.urls import path

from . import views
app_name = 'tools'
urlpatterns = [
   # url(r'^', views.index, name='index'),
    path('', views.list_category_groups, name='index'),
    path('tools_and_methods/', views.list_tools, name='list_tools'), 
    path('tools_and_methods/<int:tool_id>/', views.show_tool, name='show'),
    path('tools_and_methods/follow/<int>:tool_id/', views.follow_tool, name='follow'),
    path('tools_and_methods/unfollow/<int:tool_id>/', views.unfollow_tool, name='unfollow'),
    path('follow/<int:category_group_id>/', views.follow_category_group, name='follow_work_area'),
    path('unfollow/<int:category_group_id>/',
         views.unfollow_category_group, name='unfollow_work_area'),
    path('stories_of_change/story/add/tool/<int:tool_id>/', views.add_story, name='add_story'),
    path('stories_of_change/story/add/workarea/<int:category_group_id>/', views.add_workarea_story, name='add_workarea_story'),
    path('stories_of_change/', views.show_all_stories, name='show_all_stories'), 
    path('stories_of_change/story/<int:story_id>/', views.show_story, name='show_story'),
    path('stories_of_change/story/edit/<int:story_id>/', views.edit_story, name='edit_story'),
    path('toolboxes/show/<int:cat_id>/', views.show_category, name='show_category'),
    path('show/<int:category_group_id>/', views.show_categorygroup, name='show_categorygroup'),
    path('suggestion/<string>/<int>/', views.add_suggestion, name='add_suggestion'),
    path('overview/edit/<string>/', views.edit_overview, name='edit_overview'),
]
