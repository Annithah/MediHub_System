from django import forms
from .models import MedicalRecord, PatientProfile, Billing, PatientNotification

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'address', 'phone_number', 'emergency_contact', 'blood_group']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['date', 'diagnosis', 'treatment']  # Removed 'notes'

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['date', 'amount', 'description', 'status']

class PatientNotificationForm(forms.ModelForm):
    class Meta:
        model = PatientNotification
        fields = ['message', 'type']
