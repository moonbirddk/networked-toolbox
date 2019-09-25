
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path


from search.views import search_page, homepage

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('trumbowyg/', include('trumbowyg.urls')),
    path('hijack/', include('hijack.urls', namespace='hijack')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('thematicareas/', include('tools.urls', namespace='tools')),
    path('resources/', include('resources.urls', namespace='resources')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('search/', include('search.urls', namespace='search')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('menus/', include('menus.urls', namespace='menus')),
    path('activity/', include('activities.urls', namespace='activities')),
    path('search/', search_page, name='search_page'),
    path('notifications/', include('user_notifications.urls', namespace='notifications')), 
    path('', homepage, name='homepage')
] + static(settings.STATIC_URL_PATTERN, document_root=settings.STATIC_ROOT) +\
        static(settings.MEDIA_URL_PATTERN, document_root=settings.MEDIA_ROOT)

