from django.contrib import admin
from .models import Specialty, Doctor, Appointment, Feedback, PDFMessage

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
    list_display = ('patient', 'doctor', 'date_time', 'status', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'purpose')
    list_filter = ('status', 'date_time', 'created_at')
    date_hierarchy = 'date_time'
    raw_id_fields = ('patient', 'doctor')
    ordering = ('-date_time',)
    list_editable = ('status',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'patient', 'rating', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'comment')
    list_filter = ('rating', 'created_at')
    raw_id_fields = ('appointment', 'patient')
    ordering = ('-created_at',)

@admin.register(PDFMessage)
class PDFMessageAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'pdf_file', 'created_at')
    search_fields = ('appointment__id',)
    list_filter = ('created_at',)
    raw_id_fields = ('appointment',)
    ordering = ('-created_at',)