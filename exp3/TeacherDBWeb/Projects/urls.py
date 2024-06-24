from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_manage, name='projectManage'),
    path('add/', views.project_add, name='projectAdd'),
    path('search/', views.project_search, name='projectSearch'),
    path('edit/<str:id>', views.project_edit, name='projectEdit'),
    path('delete/<str:id>', views.project_delete, name='projectDelete'),
]