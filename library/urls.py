"""
library urlconf

library:url_name
"""

from django.urls import path

from .views import (
    document_index, 
    show_library_item, 
    course_signoff, 
    course_signup
)

app_name = 'library'
urlpatterns = [
    # url(r'^', views.index, name='index'),
    path('', document_index, name='document_index'),
    path('documents/<int:document_id>/', show_library_item, name='show_librarydocument'),
    path('video_resources/<int:document_id>/', show_library_item, name='show_videoresource'),
    path('courses/<int:document_id>/', show_library_item, name='show_onlinecourse'),
    path('<int:id>/signup_user/', course_signup, name='signup_course'),
    path('<int:id>/signoff_user/', course_signoff, name='signoff_course'),
    #path('signoff_user/', show_event, name='show_event'),

]
