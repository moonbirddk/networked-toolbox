from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^tools/$', views.ToolSearchView.as_view(), name='tool_results'),
    url(r'^profiles/$', views.ProfileSearchView.as_view(), name='profile_results'),
    url(r'^stories/$', views.StorySearchView.as_view(), name='story_results'),
]
