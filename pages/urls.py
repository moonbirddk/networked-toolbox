from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
  
    path('<string>/', views.show_page, name='show_page'),
]
