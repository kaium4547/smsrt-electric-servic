# smart_electric_service/services/views.py
from django.shortcuts import render, get_object_or_404
from .models import Service

def service_list(request):
    # For now, return the static services page
    return render(request, 'services.html')

def service_detail(request, id, slug):
    # For now, return the static services page
    return render(request, 'services.html')