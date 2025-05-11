from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PatientProfile, MedicalRecord, Billing, PatientNotification
from .forms import PatientProfileForm, MedicalRecordForm, BillingForm
from appointment_app.models import Appointment

@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')

    try:
        profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        profile = PatientProfile.objects.create(user=request.user)

    appointments = Appointment.objects.filter(patient=request.user).order_by('-date_time')
    records = MedicalRecord.objects.filter(patient=request.user).order_by('-date')
    bills = Billing.objects.filter(patient=request.user).order_by('-date')
    notifications = PatientNotification.objects.filter(patient=request.user).order_by('-sent_at')

    return render(request, 'patient_management_app/patient_dashboard.html', {
        'profile': profile,
        'appointments': appointments,
        'records': records,
        'bills': bills,
        'notifications': notifications,
    })

@login_required
def edit_profile(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')

    try:
        profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        profile = PatientProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('patient_management_app:patient_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientProfileForm(instance=profile)

    return render(request, 'patient_management_app/edit_profile.html', {'form': form})

@login_required
def view_medical_record(request, record_id):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')

    record = get_object_or_404(MedicalRecord, id=record_id, patient=request.user)
    return render(request, 'patient_management_app/view_medical_record.html', {'record': record})

@login_required
def view_billing(request, bill_id):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')

    bill = get_object_or_404(Billing, id=bill_id, patient=request.user)
    return render(request, 'patient_management_app/view_billing.html', {'bill': bill})

@login_required
def mark_notification_read(request, notification_id):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')

    notification = get_object_or_404(PatientNotification, id=notification_id, patient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('patient_management_app:patient_dashboard')