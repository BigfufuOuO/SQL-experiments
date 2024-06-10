from django.urls import path
from . import views

urlpatterns = [
    path('', views.paper_manage, name='paperManage'),
    path('add/', views.paper_add, name='paperAdd'),
]