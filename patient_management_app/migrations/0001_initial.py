# Generated by Django 5.2.1 on 2025-05-11 22:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointment_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Billing date.')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Billing amount.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(help_text='Billing description.')),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', help_text='Billing status.', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the billing was created.')),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pm_billings', to='appointment_app.appointment')),
                ('patient', models.ForeignKey(limit_choices_to={'role': 'patient'}, on_delete=django.db.models.deletion.CASCADE, related_name='pm_billings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Billing',
                'verbose_name_plural': 'Billings',
                'db_table': 'patient_billings',
            },
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Date of the medical record.')),
                ('diagnosis', models.TextField(help_text='Diagnosis details.')),
                ('treatment', models.TextField(blank=True, help_text='Treatment details.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the record was created.')),
                ('doctor', models.ForeignKey(limit_choices_to={'role': 'doctor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pm_managed_records', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(limit_choices_to={'role': 'patient'}, on_delete=django.db.models.deletion.CASCADE, related_name='pm_medical_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Medical Record',
                'verbose_name_plural': 'Medical Records',
                'db_table': 'medical_records',
            },
        ),
        migrations.CreateModel(
            name='PatientNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Notification message.')),
                ('type', models.CharField(choices=[('reminder', 'Reminder'), ('confirmation', 'Confirmation'), ('billing', 'Billing')], help_text='Type of notification.', max_length=20)),
                ('sent_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the notification was sent.')),
                ('is_read', models.BooleanField(default=False, help_text='Whether the notification has been read.')),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pm_notifications', to='appointment_app.appointment')),
                ('patient', models.ForeignKey(limit_choices_to={'role': 'patient'}, on_delete=django.db.models.deletion.CASCADE, related_name='pm_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Patient Notification',
                'verbose_name_plural': 'Patient Notifications',
                'db_table': 'patient_notifications',
            },
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, help_text="Patient's date of birth.", null=True)),
                ('address', models.TextField(blank=True, help_text="Patient's address.", null=True)),
                ('phone_number', models.CharField(blank=True, help_text="Patient's phone number.", max_length=15, null=True)),
                ('emergency_contact', models.CharField(blank=True, help_text='Emergency contact number.', max_length=15, null=True)),
                ('blood_group', models.CharField(blank=True, help_text="Patient's blood group (e.g., A+, O-).", max_length=5, null=True)),
                ('user', models.OneToOneField(limit_choices_to={'role': 'patient'}, on_delete=django.db.models.deletion.CASCADE, related_name='pm_patient_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Patient Profile',
                'verbose_name_plural': 'Patient Profiles',
                'db_table': 'patient_profiles',
            },
        ),
    ]
