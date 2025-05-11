from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from auth_application.models import User

class Specialty(models.Model):
    """
    Model to store medical specialties for doctors.
    """
    name = models.CharField(max_length=100, unique=True, help_text="The name of the medical specialty.")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the specialty.")

    class Meta:
        db_table = 'specialties'
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'

    def __str__(self):
        return self.name

class Doctor(models.Model):
    """
    Model to store doctor profiles, linked to a User with the 'doctor' role.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', limit_choices_to={'role': 'doctor'})
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True, help_text="The doctor's unique license number.")
    qualification = models.TextField(blank=True, null=True, help_text="The doctor's qualifications.")
    experience_years = models.IntegerField(validators=[MinValueValidator(0)], default=0, help_text="Years of experience.")
    hospital_affiliation = models.CharField(max_length=255, blank=True, null=True, help_text="Affiliated hospital name.")
    profile_image = models.ImageField(upload_to='doctor_images/', null=True, blank=True, help_text="Profile image of the doctor.")

    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Appointment(models.Model):
    """
    Model to manage patient appointments with doctors.
    """
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='patient_appointments', limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor_appointments', limit_choices_to={'role': 'doctor'})
    date_time = models.DateTimeField(help_text="Scheduled date and time of the appointment.")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending',
        help_text="Current status of the appointment."
    )
    purpose = models.TextField(blank=True, null=True, help_text="Reason or purpose of the appointment.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def save(self, *args, **kwargs):
        """Validate role constraints before saving."""
        if self.patient and self.patient.role != 'patient':
            raise ValueError("Patient must have role 'patient'")
        if self.doctor and self.doctor.role != 'doctor':
            raise ValueError("Doctor must have role 'doctor'")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.first_name} on {self.date_time}"

class Feedback(models.Model):
    """
    Model to store patient feedback for appointments.
    """
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='feedback')
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='feedbacks', limit_choices_to={'role': 'patient'})
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rating from 1 to 5.")
    comment = models.TextField(blank=True, null=True, help_text="Optional feedback comment.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def save(self, *args, **kwargs):
        """Validate patient role before saving."""
        if self.patient and self.patient.role != 'patient':
            raise ValueError("Feedback provider must have role 'patient'")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback for Appointment {self.appointment_id}"

class PDFMessage(models.Model):
    """
    Model to store PDF messages associated with appointments.
    """
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='pdf_message')
    pdf_file = models.FileField(upload_to='appointment_pdfs/', validators=[FileExtensionValidator(['pdf'])], help_text="PDF file associated with the appointment.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pdf_messages'
        verbose_name = 'PDF Message'
        verbose_name_plural = 'PDF Messages'

    def __str__(self):
        return f"PDF for Appointment {self.appointment_id}"