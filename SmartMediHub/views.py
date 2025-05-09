from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, AppointmentForm
from .models import User, Doctor, Appointment

# Example view (replace with your actual views)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Add authentication logic
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})

