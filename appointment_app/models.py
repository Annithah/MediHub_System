from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from auth_application.models import User

class Specialty(models.Model):
    """
    Model to store medical specialties for doctors.
    """
    SPECIALTY_CHOICES = [
        ('general_surgery', 'General Surgery'),
        ('pediatrics', 'Pediatrics'),  
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('anesthesiology', 'Anesthesiology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('obstetrics_gynecology', 'Obstetrics and Gynecology'),
        ('urology', 'Urology'),
        ('gastroenterology', 'Gastroenterology'),
        ('endocrinology', 'Endocrinology'),
        ('pulmonology', 'Pulmonology'),
        ('nephrology', 'Nephrology'),
        ('rheumatology', 'Rheumatology'),
        ('infectious_diseases', 'Infectious Diseases'),
        ('ophthalmology', 'Ophthalmology'),
        ('otolaryngology', 'Otolaryngology'),
        ('plastic_surgery', 'Plastic Surgery'),
        ('pathology', 'Pathology'),
        ('family_medicine', 'Family Medicine'),
        ('sports_medicine', 'Sports Medicine'),
        ('geriatrics', 'Geriatrics'),
        ('other', 'Other')
    ]
    name = models.CharField(max_length=100, unique=True, help_text="The name of the medical specialty.", choices=SPECIALTY_CHOICES)
    description = models.TextField(blank=True, null=True, help_text="Optional description of the specialty.")

    class Meta:
        db_table = 'specialties'
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'

    def __str__(self):
        return self.name


class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('general_surgery', 'General Surgery'),
        ('pediatrics', 'Pediatrics'),  
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('anesthesiology', 'Anesthesiology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('obstetrics_gynecology', 'Obstetrics and Gynecology'),
        ('urology', 'Urology'),
        ('gastroenterology', 'Gastroenterology'),
        ('endocrinology', 'Endocrinology'),
        ('pulmonology', 'Pulmonology'),
        ('nephrology', 'Nephrology'),
        ('rheumatology', 'Rheumatology'),
        ('infectious_diseases', 'Infectious Diseases'),
        ('ophthalmology', 'Ophthalmology'),
        ('otolaryngology', 'Otolaryngology'),
        ('plastic_surgery', 'Plastic Surgery'),
        ('pathology', 'Pathology'),
        ('family_medicine', 'Family Medicine'),
        ('sports_medicine', 'Sports Medicine'),
        ('geriatrics', 'Geriatrics'),
        ('other', 'Other')
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    specialty = models.CharField(
        max_length=100,
        choices=SPECIALTY_CHOICES,
        help_text="The medical specialty of the doctor.",
        default='general_surgery'
    )
    license_number = models.CharField(max_length=50, unique=True)
    qualification = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    hospital_affiliation = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='doctor_images/',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class Appointment(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patient_appointments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='doctor_appointments'
    )
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending',
        help_text="Current status of the appointment."
    )
    purpose = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def clean(self):
        if self.patient and self.patient.role != 'patient':
            raise ValidationError({'patient': "Patient must have role 'patient'"})
        super().clean()

    def __str__(self):
        
        patient_name = f"{self.patient.first_name} {self.patient.last_name}"
        doctor_name  = f"Dr. {self.doctor.user.first_name} {self.doctor.user.last_name}"
        date_str     = self.date_time.strftime('%Y-%m-%d %H:%M')
        return f"Appointment: {patient_name} ↔ {doctor_name} on {date_str}"

class Feedback(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='feedbacks'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def clean(self):
        if self.patient and self.patient.role != 'patient':
            raise ValidationError({'patient': "Feedback provider must have role 'patient'"})
        super().clean()

    def __str__(self):
        return f"Feedback for Appointment #{self.appointment_id}"


class Availability(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        db_table = 'availability'

    def clean(self):
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError({'end_time': "End time must be after start time"})
        super().clean()

    def __str__(self):
        return f"Availability for {self.doctor} from {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    message = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=[
            ('reminder', 'Reminder'),
            ('confirmation', 'Confirmation'),
            ('cancellation', 'Cancellation'),
        ]
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message[:50]}"


class PDFMessage(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='pdf_message'
    )
    pdf_file = models.FileField(
        upload_to='appointment_pdfs/',
        validators=[FileExtensionValidator(['pdf'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pdf_messages'
        verbose_name = 'PDF Message'
        verbose_name_plural = 'PDF Messages'

    def __str__(self):
        return f"PDF for Appointment #{self.appointment_id}"


class Billing(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='billings'
    )
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'billing'

    def clean(self):
        if self.patient and self.patient.role != 'patient':
            raise ValidationError({'patient': "Billing must be for a user with role 'patient'"})
        super().clean()

    def __str__(self):
        return f"Billing for {self.patient.email}: {self.amount}"
