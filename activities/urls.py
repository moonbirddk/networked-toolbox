from django.urls import path


from . import views
app_name = 'activities'

urlpatterns = [
    
    path('', views.list_all, name='list_all'),
]
