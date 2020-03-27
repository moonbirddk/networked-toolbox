from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
  
    path('<slug:page_slug>/', views.show_page, name='show_page'),
]
