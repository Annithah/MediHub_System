from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    
    groups = models.ManyToManyField(
        Group,
        related_name='smartmedi_users', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='smartmedi_user_permissions',  
        blank=True
    )

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    blood_type = models.CharField(max_length=5)
    medical_history = models.TextField()
    allergies = models.TextField()

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
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # specialization = models.CharField(max_length=100)
    # license_no = models.CharField(max_length=50)
    # department = models.CharField(max_length=100)
    # available_days = models.CharField(max_length=100)

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100)
    shift = models.CharField(max_length=50)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled")
    ])
    purpose = models.TextField()

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    medication = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField()

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ("Paid", "Paid"),
        ("Unpaid", "Unpaid")
    ])

class HospitalService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    capacity = models.IntegerField()
