from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.service_request_detail, name='service_request_detail'),
    path('<int:pk>/add-comment/', views.add_comment, name='add_comment'),
]