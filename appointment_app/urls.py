from django.urls import path
from . import views 

app_name = 'appointment_app'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('', views.view_appointments, name='view_appointments'),
    path('availability/add/', views.add_availability, name='add_availability'),
    path('availability/', views.view_availabilities, name='view_availabilities'),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    
    path('send-pdf/<int:appointment_id>/', views.send_pdf_message, name='send_pdf_message'),

]