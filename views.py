from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from .models import *
from .forms import *

# Index View
def index(request):
    return render(request, 'index.html')

    




