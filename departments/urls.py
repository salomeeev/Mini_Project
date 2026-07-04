from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.department_list, name='list'),
    path('add/', views.department_add, name='add'),
    path('edit/<int:pk>/', views.department_edit, name='edit'),
    path('delete/<int:pk>/', views.department_delete, name='delete'),
]
