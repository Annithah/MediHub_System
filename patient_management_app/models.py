from django.db import models
from django.core.validators import MinValueValidator
from auth_application.models import User
from appointment_app.models import Appointment

class PatientProfile(models.Model):
    """
    Model to store additional patient profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', limit_choices_to={'role': 'patient'})
    date_of_birth = models.DateField(null=True, blank=True, help_text="Patient's date of birth.")
    address = models.TextField(blank=True, null=True, help_text="Patient's address.")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Patient's phone number.")
    emergency_contact = models.CharField(max_length=15, blank=True, null=True, help_text="Emergency contact number.")
    blood_group = models.CharField(max_length=5, blank=True, null=True, help_text="Patient's blood group (e.g., A+, O-).")

    class Meta:
        db_table = 'patient_profiles'
        verbose_name = 'Patient Profile'
        verbose_name_plural = 'Patient Profiles'

    def __str__(self):
        return f"Profile of {self.user.first_name} {self.user.last_name}"

class MedicalRecord(models.Model):
    """
    Model to store patient medical records.
    """
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records', limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_records', limit_choices_to={'role': 'doctor'})
    date = models.DateField(auto_now_add=False, help_text="Date of the medical record.")
    diagnosis = models.TextField(help_text="Diagnosis details.")
    treatment = models.TextField(blank=True, null=True, help_text="Treatment details.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the record was created.")

    class Meta:
        db_table = 'medical_records'
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'

    def __str__(self):
        return f"Record for {self.patient.first_name} on {self.date}"

class Billing(models.Model):
    """
    Model to store patient billing information.
    """
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billings', limit_choices_to={'role': 'patient'})
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='billings')
    date = models.DateField(auto_now_add=False, help_text="Billing date.")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Billing amount.")
    description = models.TextField(help_text="Billing description.")
    status = models.CharField(
        max_length=20,
        choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')],
        default='Unpaid',
        help_text="Billing status."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the billing was created.")

    class Meta:
        db_table = 'patient_billings'
        verbose_name = 'Billing'
        verbose_name_plural = 'Billings'

    def save(self, *args, **kwargs):
        """Validate that the patient has the correct role."""
        if self.patient and self.patient.role != 'patient':
            raise ValueError("Billing must be for a user with role 'patient'")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Billing for {self.patient.first_name}: {self.amount}"

class PatientNotification(models.Model):
    """
    Model to store notifications for patients.
    """
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', limit_choices_to={'role': 'patient'})
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    message = models.TextField(help_text="Notification message.")
    type = models.CharField(
        max_length=20,
        choices=[('reminder', 'Reminder'), ('confirmation', 'Confirmation'), ('billing', 'Billing')],
        help_text="Type of notification."
    )
    sent_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the notification was sent.")
    is_read = models.BooleanField(default=False, help_text="Whether the notification has been read.")

    class Meta:
        db_table = 'patient_notifications'
        verbose_name = 'Patient Notification'
        verbose_name_plural = 'Patient Notifications'

    def __str__(self):
        return f"Notification for {self.patient.first_name}: {self.message[:50]}"