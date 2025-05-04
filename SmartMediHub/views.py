from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .models import *
from .forms import *

# Index View
def index(request):
    return render(request, 'index.html')  # Ensure you have an 'index.html' file in your templates folder

# Doctor Signup View
def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Doctor.objects.create(user=user)
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSignUpForm()
    return render(request, 'registration/doctor_signup.html', {'form': form})

# Patient Signup View
def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(user=user)
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'registration/patient_signup.html', {'form': form})

# Patient Dashboard
@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('login')
    appointments = Appointment.objects.filter(patient=request.user.patient)
    prescriptions = Prescription.objects.filter(patient=request.user.patient)
    bills = Billing.objects.filter(patient=request.user.patient)
    return render(request, 'patient_dashboard.html', {
        'appointments': appointments,
        'prescriptions': prescriptions,
        'bills': bills
    })

# Doctor Dashboard
@login_required
@user_passes_test(lambda u: u.is_doctor)
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
@user_passes_test(lambda u: u.is_admin)
def admin_dashboard(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()
    return render(request, 'admin.html', {
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
    return render(request, 'book_appointment.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_doctor)
def manage_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        appointment.status = status
        appointment.save()
        return redirect('doctor_dashboard')
    return render(request, 'manage_appointment.html', {'appointment': appointment})

# Prescription Views
@login_required
@user_passes_test(lambda u: u.is_doctor)
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

# Billing View (new)
@login_required
def billing_list(request):
    if request.user.is_patient:
        bills = Billing.objects.filter(patient=request.user.patient)
    elif request.user.is_doctor:
        bills = Billing.objects.all()  # Or customize
    else:
        bills = Billing.objects.none()
    return render(request, 'billing_list.html', {'bills': bills})
