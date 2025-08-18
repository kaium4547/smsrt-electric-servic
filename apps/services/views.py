# smart_electric_service/services/views.py
from django.shortcuts import render, get_object_or_404
from .models import Service

def service_list(request):
    services = Service.objects.filter(available=True).prefetch_related('features')
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, id, slug):
    service = get_object_or_404(Service, id=id, slug=slug, available=True)
    features = service.features.all()
    return render(request, 'services/service_detail.html', {'service': service, 'features': features})