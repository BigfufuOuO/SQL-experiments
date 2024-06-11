from django.urls import path
from . import views

urlpatterns = [
    path('', views.paper_manage, name='paperManage'),
    path('add/', views.paper_add, name='paperAdd'),
    path('search/', views.paper_search, name='paperSearch'),
    path('edit/<int:id>', views.paper_edit, name='paperEdit'),
]