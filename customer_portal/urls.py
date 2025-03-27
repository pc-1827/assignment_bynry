from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='customer_dashboard'),
    path('requests/', views.request_list, name='customer_request_list'),
    path('requests/new/', views.create_request, name='create_request'),
]