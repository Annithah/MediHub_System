from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from auth_application.models import User
from .models import Doctor, Appointment
from .forms import AppointmentForm
from patient_management_app.models import Billing, PatientNotification, MedicalRecord

@login_required
def dashboard(request):
    if request.user.role not in ['patient', 'doctor']:
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')
    
    if request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user).order_by('-date_time')
        records = MedicalRecord.objects.filter(patient=request.user).order_by('-date')
        bills = Billing.objects.filter(patient=request.user).order_by('-date')
        notifications = PatientNotification.objects.filter(patient=request.user).order_by('-sent_at')
        return render(request, 'appointment_app/dashboard.html', {
            'appointments': appointments,
            'records': records,
            'bills': bills,
            'notifications': notifications,
        })
    elif request.user.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user).order_by('-date_time')
        return render(request, 'appointment_app/dashboard.html', {'appointments': appointments})

@login_required
def list_doctors(request):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('patient_management_app:patient_dashboard')
    
    doctors = Doctor.objects.all()
    return render(request, 'appointment_app/list_doctors.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('patient_management_app:patient_dashboard')
    
    try:
        selected_doctor = Doctor.objects.get(user__id=doctor_id)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('appointment_app:list_doctors')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = selected_doctor.user
            appointment.save()
            
            Billing.objects.create(
                patient=request.user,
                appointment=appointment,
                amount=100.00,
                description=f"Consultation fee for appointment with Dr. {selected_doctor.user.first_name} on {appointment.date_time}",
                status='Unpaid'
            )
            PatientNotification.objects.create(
                patient=request.user,
                appointment=appointment,
                message=f"Your appointment with Dr. {selected_doctor.user.first_name} on {appointment.date_time} has been booked.",
                type='confirmation'
            )
            
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_management_app:patient_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {'doctor': selected_doctor.user.id}
        form = AppointmentForm(initial=initial_data)
        form.fields['doctor'].widget = form.fields['doctor'].hidden_widget()
    return render(request, 'appointment_app/book_appointment.html', {'form': form, 'selected_doctor': selected_doctor})

@login_required
def approve_appointment(request, appointment_id):
    if request.user.role != 'doctor':
        messages.error(request, 'Only doctors can approve appointments.')
        return redirect('appointment_app:dashboard')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    if request.method == 'POST':
        if appointment.status == 'pending':
            appointment.status = 'confirmed'
            appointment.save()
            PatientNotification.objects.create(
                patient=appointment.patient,
                appointment=appointment,
                message=f"Your appointment with Dr. {appointment.doctor.first_name} on {appointment.date_time} has been confirmed.",
                type='confirmation'
            )
            messages.success(request, 'Appointment confirmed successfully!')
        else:
            messages.error(request, 'Appointment cannot be confirmed.')
        return redirect('appointment_app:dashboard')
    
    return render(request, 'appointment_app/approve_appointment.html', {'appointment': appointment})

@login_required
def view_appointments(request):
    if request.user.role not in ['patient', 'doctor']:
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')
    
    if request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user).order_by('-date_time')
    else:
        appointments = Appointment.objects.filter(doctor=request.user).order_by('-date_time')
    
    return render(request, 'appointment_app/view_appointments.html', {'appointments': appointments})