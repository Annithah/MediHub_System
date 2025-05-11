from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .models import *
from .forms import *


def index(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('appointment_app:dashboard')

    def get_success_url(self):
        
        return self.success_url

    def form_invalid(self, form):
        
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)