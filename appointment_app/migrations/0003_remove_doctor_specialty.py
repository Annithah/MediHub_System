# Generated by Django 5.2.1 on 2025-05-12 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_app', '0002_alter_specialty_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='specialty',
        ),
    ]
