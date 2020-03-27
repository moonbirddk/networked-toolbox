from django.urls import path

from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_page, name='homepage'),
    path('tools/', views.ToolSearchView.as_view(), name='tool_results'),
    path('profiles/', views.ProfileSearchView.as_view(), name='profile_results'),
    path('stories/', views.StorySearchView.as_view(), name='story_results'),
]
