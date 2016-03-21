"""
tools urlconf

tools:url_name
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\d+)/$', views.show, name='show'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/(\d+)/$', views.edit, name='edit'),
    url(r'^follow/(\d+)/$', views.follow, name='follow'),
    url(r'^unfollow/(\d+)/$', views.unfollow, name='unfollow'),
    url(r'^story/add/tool/(\d+)/$', views.add_story, name='add_story'),
    url(r'^story/(\d+)/$', views.show_story, name='show_story'),

    url(r'^categories/$', views.list_categories, name='list_categories'),
    url(r'^categories/add/$', views.add_category, name='add_category'),
    url(r'^categories/show/(\d+)/$', views.show_category, name='show_category'),
    url(r'^categories/edit/(\d+)/$', views.edit_category, name='edit_category'),
    url(r'^categories/delete/(\d+)/$', views.delete_category, name='delete_category'),

    url(r'^category-groups/add/$', views.add_categorygroup, name='add_categorygroup'),
    url(r'^category-groups/edit/(\d+)/$', views.edit_categorygroup, name='edit_categorygroup'),
    url(r'^category-groups/delete/(\d+)/$', views.delete_categorygroup, name='delete_categorygroup'),

    url(r'^suggestion/([a-z]+)/(\d+)/$', views.add_suggestion, name='add_suggestion'),

    url(r'^overview/edit/([a-z]+)/$', views.edit_overview, name='edit_overview'),
]
