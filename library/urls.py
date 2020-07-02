"""
library urlconf

library:url_name
"""

from django.urls import path

from .views import (
    document_index, 
    show_library_item, 
)

app_name = 'library'
urlpatterns = [
    # url(r'^', views.index, name='index'),
    path('', document_index, name='document_index'),
    path('documents/<int:document_id>/', show_library_item, name='show_librarydocument'),
    path('/video_resources/<int:document_id>/', show_library_item, name='show_videoresource'),
    path('courses/<int:document_id>/', show_library_item, name='show_onlinecourse'),
    # path('<int:id>/signup_user/', event_signup, name='signup_event'),
    # path('<int:id>/signoff_user/', event_signoff, name='signoff_event'),
    # #path('signoff_user/', show_event, name='show_event'),

]
