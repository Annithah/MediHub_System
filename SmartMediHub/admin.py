from django.contrib import admin
from .models import User, Specialty, Doctor, Appointment, Feedback, Availability, Notification, PDFMessage, Billing

admin.site.register(User)
admin.site.register(Specialty)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Feedback)
admin.site.register(Availability)
admin.site.register(Notification)
admin.site.register(PDFMessage)
admin.site.register(Billing)