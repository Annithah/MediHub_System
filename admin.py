from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(MedicalRecord)
admin.site.register(Billing)
admin.site.register(HospitalService)