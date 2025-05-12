from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from auth_application.models import User
from .models import Doctor, Appointment, Availability, PDFMessage
from .forms import AppointmentForm, AvailabilityForm, PDFMessageForm
from patient_management_app.models import *

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
        return render(request, 'dashboard.html', {
            'appointments': appointments,
            'records': records,
            'bills': bills,
            'notifications': notifications,
        })
    elif request.user.role == 'doctor':
        doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor).order_by('-date_time')
        context = {'appointments': appointments}
    
    return render(request, 'dashboard.html', context)

@login_required
def list_doctors(request):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('patient_management_app:patient_dashboard')
    
    doctors = Doctor.objects.all()
    return render(request, 'list_doctors.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('patient_management_app:patient_dashboard')
    
    try:
        selected_doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('appointment_app:list_doctors')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = selected_doctor

            availability = Availability.objects.filter(
                doctor=appointment.doctor,
                start_time__lte=appointment.date_time,
                end_time__gte=appointment.date_time,
                is_booked=False
            ).first()
            if not availability:
                messages.error(request, 'Selected time slot is not available.')
                return render(request, 'book_appointment.html', {'form': form, 'selected_doctor': selected_doctor})
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
            return redirect('appointment_app:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {'doctor': selected_doctor.user.id}
        form = AppointmentForm(initial=initial_data)
        form.fields['doctor'].widget = form.fields['doctor'].hidden_widget()  
    return render(request, 'book_appointment.html', {'form': form, 'selected_doctor': selected_doctor})

@login_required
def approve_appointment(request, appointment_id):
    if request.user.role != 'doctor':
        messages.error(request, 'Only doctors can approve appointments.')
        return redirect('appointment_app:dashboard')

    doctor = Doctor.objects.get(user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    if request.method == 'POST':
        if appointment.status == 'pending':
            appointment.status = 'confirmed'
            appointment.save()
            PatientNotification.objects.create(
                patient=appointment.patient,
                appointment=appointment,
                message=f"Your appointment with Dr. {appointment.doctor.user.first_name} on {appointment.date_time} has been confirmed.",
                type='confirmation'
            )
            messages.success(request, 'Appointment confirmed successfully!')
        else:
            messages.error(request, 'Appointment cannot be confirmed.')
        return redirect('appointment_app:dashboard')
    
    return render(request, 'approve_appointment.html', {'appointment': appointment})

@login_required
def view_appointments(request):
    if request.user.role not in ['patient', 'doctor']:
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')
    
    if request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user).order_by('-date_time')
    else:
        try:
            doctor = Doctor.objects.get(user=request.user)
            appointments = Appointment.objects.filter(doctor=doctor).order_by('-date_time')
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('auth_application:login')
    
    return render(request, 'view_appointments.html', {'appointments': appointments})

@login_required
def add_availability(request):
    if request.user.role != 'doctor':
        messages.error(request, "Only doctors can add availability.")
        return redirect('appointment_app:dashboard')

    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('appointment_app:dashboard')

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = doctor
            availability.save()
            messages.success(request, "Availability added successfully.")
            return redirect('appointment_app:view_availabilities')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AvailabilityForm()

    return render(request, 'add_availability.html', {'form': form})

@login_required
def view_availabilities(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access restricted to doctors only.")
        return redirect('appointment_app:dashboard')

    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('appointment_app:dashboard')

    availabilities = Availability.objects.filter(doctor=doctor).order_by('start_time')
    return render(request, 'view_availabilities.html', {'availabilities': availabilities})



@login_required
def send_pdf_message(request, appointment_id):
    if request.user.role != 'doctor':
        messages.error(request, 'Only doctors can send PDF messages.')
        return redirect('appointment_app:dashboard')

    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('appointment_app:dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    if request.method == 'POST':
        form = PDFMessageForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_message = form.save(commit=False)
            pdf_message.appointment = appointment
            pdf_message.save()
            messages.success(request, "PDF message sent to the patient.")
            return redirect('appointment_app:dashboard')
        else:
            messages.error(request, "Please upload a valid PDF file.")
    else:
        form = PDFMessageForm()

    return render(request, 'pdf_report.html', {
        'form': form,
        'appointment': appointment
    })
