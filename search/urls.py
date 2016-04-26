from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^tool/$',
        views.ToolSearchView.as_view(),
        name='tool_results'),
]
