from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from auth_application.models import User
from .models import Appointment, Availability
from .forms import AppointmentForm

@login_required
def dashboard(request):
    if request.user.role not in ['patient', 'doctor']:
        messages.error(request, 'Access denied: Invalid role.')
        return redirect('auth_application:login')
    
    context = {'user_role': request.user.role}
    
    if request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')
        context['appointments'] = appointments
    elif request.user.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user).order_by('-appointment_date')
        context['appointments'] = appointments
    
    return render(request, 'dashboard.html', context)

@login_required
def book_appointment(request):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('appointment_app:dashboard')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            # Validate doctor role
            if appointment.doctor.role != 'doctor':
                messages.error(request, 'Selected user is not a doctor.')
                return render(request, 'book_appointment.html', {'form': form})
            # Check availability
            availability = Availability.objects.filter(
                doctor=appointment.doctor,
                start_time__lte=appointment.appointment_date,
                end_time__gte=appointment.appointment_date,
                is_booked=False
            ).first()
            if not availability:
                messages.error(request, 'Selected time slot is not available.')
                return render(request, 'book_appointment.html', {'form': form})
            appointment.save()
            availability.is_booked = True
            availability.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointment_app:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm()
        # Limit doctor choices to users with role 'doctor'
        form.fields['doctor'].queryset = User.objects.filter(role='doctor')
    return render(request, 'book_appointment.html', {'form': form})

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
        appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')
    else:  # doctor
        appointments = Appointment.objects.filter(doctor=request.user).order_by('-appointment_date')
    
    return render(request, 'view_appointments.html', {'appointments': appointments})