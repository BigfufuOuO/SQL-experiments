from django.urls import path
from . import views

urlpatterns = [
    path('', views.info_index),
    path('search/', views.info_search),
]