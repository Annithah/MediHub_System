from django.urls import path
from . import views

app_name = 'appointment_app'

urlpatterns = [
    path('appointment/', views.dashboard, name='dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('', views.view_appointments, name='view_appointments'),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
]