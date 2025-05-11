from django.contrib import admin
from .models import Specialization, Doctor, Schedule, Appointment, DoctorDocument

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'user', 'specialization', 'email', 'phone',
        'license_number', 'years_of_experience', 'is_active', 'date_joined'
    )
    list_filter = ('specialization', 'is_active', 'years_of_experience')
    search_fields = ('full_name', 'email', 'license_number', 'user__username')
    readonly_fields = ('date_joined',)
    raw_id_fields = ('user',)
    autocomplete_fields = ('specialization',)
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'specialization', 'email', 'phone', 'address', 'profile_picture')
        }),
        ('Professional Info', {
            'fields': ('license_number', 'years_of_experience', 'is_active', 'date_joined')
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('doctor', 'day_of_week')
    search_fields = ('doctor__full_name', 'day_of_week')
    autocomplete_fields = ('doctor',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'doctor', 'patient_name', 'appointment_date', 'appointment_time',
        'status', 'created_at'
    )
    list_filter = ('doctor', 'status', 'appointment_date')
    search_fields = ('patient_name', 'doctor__full_name', 'patient_contact')
    autocomplete_fields = ('doctor',)
    readonly_fields = ('created_at',)

@admin.register(DoctorDocument)
class DoctorDocumentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'description', 'document', 'uploaded_at')
    list_filter = ('doctor',)
    search_fields = ('doctor__full_name', 'description')
    autocomplete_fields = ('doctor',)
    readonly_fields = ('uploaded_at',)