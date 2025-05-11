from django.urls import path
from . import views

app_name = 'patient_management_app'
urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('medical-record/<int:record_id>/', views.view_medical_record, name='view_medical_record'),
    path('billing/<int:bill_id>/', views.view_billing, name='view_billing'),
    path('notification/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]