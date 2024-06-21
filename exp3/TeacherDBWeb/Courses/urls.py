from django.urls import path
from . import views

urlpatterns = [
    path('add_individually/', views.course_add_individually),
    path('', views.course_manage),
    path('add/', views.course_add),
    path('search/', views.course_search),
    path('edit/<str:id>/<int:year>/<int:semester>', views.course_edit),
    path('delete/<str:id>/<int:year>/<int:semester>', views.course_delete),
]