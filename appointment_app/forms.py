from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'purpose']  # Updated to match new model fields
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


from .models import Availability

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }