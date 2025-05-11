from django.contrib import admin
from .models import MedicalRecord, Billing, PatientNotification

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'diagnosis', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'diagnosis', 'treatment')
    list_filter = ('date', 'created_at')
    raw_id_fields = ('patient', 'doctor')
    ordering = ('-date',)

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'status', 'date', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'description')
    list_filter = ('status', 'date', 'created_at')
    raw_id_fields = ('patient', 'appointment')
    ordering = ('-date',)
    list_editable = ('status',)

@admin.register(PatientNotification)
class PatientNotificationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'type', 'sent_at', 'is_read')
    search_fields = ('patient__first_name', 'patient__last_name', 'message')
    list_filter = ('type', 'is_read', 'sent_at')
    raw_id_fields = ('patient', 'appointment')
    ordering = ('-sent_at',)