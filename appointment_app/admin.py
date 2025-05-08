from django.contrib import admin
from .models import Specialty, Doctor, Appointment, Feedback, Availability, Notification, PDFMessage, Billing

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'license_number', 'experience_years', 'hospital_affiliation')
    search_fields = ('user__first_name', 'user__last_name', 'license_number', 'hospital_affiliation')
    list_filter = ('specialty', 'experience_years')
    raw_id_fields = ('user', 'specialty')
    ordering = ('user__last_name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'reason')
    list_filter = ('status', 'appointment_date', 'created_at')
    date_hierarchy = 'appointment_date'
    raw_id_fields = ('patient', 'doctor')
    ordering = ('-appointment_date',)
    list_editable = ('status',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'patient', 'rating', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'comment')
    list_filter = ('rating', 'created_at')
    raw_id_fields = ('appointment', 'patient')
    ordering = ('-created_at',)

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_time', 'end_time', 'is_booked')
    search_fields = ('doctor__first_name', 'doctor__last_name')
    list_filter = ('is_booked', 'start_time', 'end_time')
    date_hierarchy = 'start_time'
    raw_id_fields = ('doctor',)
    ordering = ('start_time',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'sent_at', 'is_read')
    search_fields = ('user__first_name', 'user__last_name', 'message')
    list_filter = ('type', 'is_read', 'sent_at')
    raw_id_fields = ('user', 'appointment')
    ordering = ('-sent_at',)

@admin.register(PDFMessage)
class PDFMessageAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'pdf_file', 'created_at')
    search_fields = ('appointment__id',)
    list_filter = ('created_at',)
    raw_id_fields = ('appointment',)
    ordering = ('-created_at',)

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'status', 'date', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'description')
    list_filter = ('status', 'date', 'created_at')
    raw_id_fields = ('patient',)
    ordering = ('-date',)
    list_editable = ('status',)