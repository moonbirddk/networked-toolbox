"""netbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
    #url(r'^hijack/', include('hijack.urls', namespace='hijack')),
    url(r'^inbox/notifications/',
        include('notifications.urls',
        namespace='notifications')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^workareas/', include('tools.urls', namespace='tools')),
    url(r'^resources/', include('resources.urls', namespace='resources')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^pages/', include('pages.urls', namespace='pages')),
    url(r'^menus/', include('menus.urls', namespace='menus')),
    url(r'^activity/', include('activities.urls', namespace='activities')),
    url(r'^$', 'search.views.homepage', name='homepage'),

] + static(settings.STATIC_URL_PATTERN, document_root=settings.STATIC_ROOT) +\
    static(settings.MEDIA_URL_PATTERN, document_root=settings.MEDIA_ROOT)
