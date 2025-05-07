from django.urls import path
from . import views

urlpatterns = [
    # Home & Authentication
    path('', views.index, name='index'),
    path('appointment/', views.index, name='appointment'),
    
]