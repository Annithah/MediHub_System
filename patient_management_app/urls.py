from django.urls import path
from . import views

app_name = 'patient_management_app'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
]