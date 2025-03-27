from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='csr_dashboard'),
    path('requests/', views.request_list, name='csr_request_list'),
    path('requests/<int:pk>/', views.request_detail, name='csr_request_detail'),
]