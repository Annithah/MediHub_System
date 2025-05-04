from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.index, name='index'),

    path('patient/signup/', views.patient_signup, name='patient_signup'),
    path('doctor/signup/', views.doctor_signup, name='doctor_signup'),
    
    # Dashboards
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Appointments
    path('appointment/book/', views.book_appointment, name='book_appointment'),
    path('appointment/manage/<int:pk>/', views.manage_appointment, name='manage_appointment'),
    
    # Prescriptions
    path('prescription/create/', views.create_prescription, name='create_prescription'),
    
    # Billing
    path('billing/', views.billing_list, name='billing_list'),
    
    # Home Page (index)
    path('index/', views.index, name='index'),  # This will map to the 'index' view
]
