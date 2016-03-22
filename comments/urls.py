from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add-comment/', views.add, name="add"),
]
