from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='list'),
    path('add/', views.employee_add, name='add'),
    path('<int:pk>/', views.employee_detail, name='detail'),
    path('edit/<int:pk>/', views.employee_edit, name='edit'),
    path('delete/<int:pk>/', views.employee_delete, name='delete'),
]
