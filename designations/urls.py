# pyrefly: ignore [missing-import]
from django.urls import path
# pyrefly: ignore [missing-import]
from . import views

app_name = 'designations'

urlpatterns = [
    path('', views.designation_list, name='list'),
    path('add/', views.designation_add, name='add'),
    path('edit/<int:pk>/', views.designation_edit, name='edit'),
    path('delete/<int:pk>/', views.designation_delete, name='delete'),
]
