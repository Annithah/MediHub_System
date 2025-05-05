from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

# Index View
def index(request):
    return render(request, 'index.html')

# Doctor Signup View
def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Doctor.objects.create(user=user)
            auth_login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSignUpForm()
    return render(request, 'doctor_signup.html', {'form': form})

# Patient Signup View
def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(user=user)
            auth_login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'login.html', {'form': form})

# Custom Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Redirect to correct dashboard
            if hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
            elif user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('index')  # fallback
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Patient Dashboard
@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient'):
        return redirect('login')
    
    appointments = Appointment.objects.filter(patient=request.user.patient)
    prescriptions = Prescription.objects.filter(patient=request.user.patient)
    bills = Billing.objects.filter(patient=request.user.patient)
    
    return render(request, 'appointment.html', {
        'appointments': appointments,
        'prescriptions': prescriptions,
        'bills': bills
    })

# Doctor Dashboard
@login_required
@user_passes_test(lambda u: hasattr(u, 'doctor'))
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor)
    patients = Patient.objects.filter(
        id__in=Appointment.objects.filter(doctor=request.user.doctor)
        .values_list('patient', flat=True)
    )
    return render(request, 'doctor_dashboard.html', {
        'appointments': appointments,
        'patients': patients
    })

# Admin Dashboard
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()
    return render(request, 'admin_dashboard.html', {
        'patients': patients,
        'doctors': doctors,
        'appointments': appointments
    })

# Appointment Views
@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})

@login_required
@user_passes_test(lambda u: hasattr(u, 'doctor'))
def manage_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return redirect('doctor_dashboard')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        appointment.status = status
        appointment.save()
        return redirect('doctor_dashboard')
    
    return render(request, 'manage_appointment.html', {'appointment': appointment})

# Prescription Views
@login_required
@user_passes_test(lambda u: hasattr(u, 'doctor'))
def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user.doctor
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'create_prescription.html', {'form': form})

# Billing View
@login_required
def billing_list(request):
    if hasattr(request.user, 'patient'):
        bills = Billing.objects.filter(patient=request.user.patient)
    elif hasattr(request.user, 'doctor'):
        bills = Billing.objects.filter(doctor=request.user.doctor)
    else:
        bills = Billing.objects.none()
    
    return render(request, 'billing_list.html', {'bills': bills})
