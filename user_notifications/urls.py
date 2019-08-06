''' Django notification urls file '''
# -*- coding: utf-8 -*-

from . import views

#if StrictVersion(get_version()) >= StrictVersion('2.0'):
#    from django.urls import re_path as pattern
#else:
from django.urls import path, re_path


urlpatterns = [
    path('', views.AllNotificationsList.as_view(), name='all'),
    path('unread/', views.UnreadNotificationsList.as_view(), name='unread'),
    path('mark-all-as-read/', views.mark_all_as_read,
            name='mark_all_as_read'),
    re_path('mark-as-read/(?P<slug>\d+)/',
            views.mark_as_read, name='mark_as_read'),
    re_path('mark-as-unread/(?P<slug>\d+)/',
            views.mark_as_unread, name='mark_as_unread'),
    re_path('delete/(?P<slug>\d+)/', views.delete, name='delete'),
    path('api/unread_count/', views.live_unread_notification_count,
            name='live_unread_notification_count'),
    path('api/all_count/', views.live_all_notification_count,
            name='live_all_notification_count'),
    path('api/unread_list/', views.live_unread_notification_list,
            name='live_unread_notification_list'),
    path('api/all_list/', views.live_all_notification_list,
            name='live_all_notification_list'),
]

app_name = '_notifications'
