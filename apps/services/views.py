# smart_electric_service/services/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceRequest


def service_list(request):
    services = Service.objects.filter(available=True).order_by('name')
    return render(request, 'services.html', { 'services': services })


def service_detail(request, id, slug):
    # Placeholder: could render a dedicated detail template later
    services = Service.objects.filter(available=True).order_by('name')
    return render(request, 'services.html', { 'services': services })


@require_POST
def create_service_request(request):
    service_id = request.POST.get('service_id') or request.POST.get('service')
    name = request.POST.get('name') or request.POST.get('customer_name')
    phone = request.POST.get('phone') or request.POST.get('customer_phone')
    email = request.POST.get('email') or request.POST.get('customer_email')
    address = request.POST.get('address')
    details = request.POST.get('details')

    if not all([service_id, name, phone, address]):
        return HttpResponseBadRequest('Missing required fields')

    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return HttpResponseBadRequest('Invalid service')

    service_request = ServiceRequest.objects.create(
        service=service,
        user=request.user if request.user.is_authenticated else None,
        customer_name=name,
        customer_phone=phone,
        customer_email=email or None,
        address=address,
        details=details or '',
    )

    return JsonResponse({
        'success': True,
        'request_id': service_request.id,
        'message': 'সার্ভিস রিকোয়েস্ট গ্রহণ করা হয়েছে! শীঘ্রই যোগাযোগ করা হবে।'
    })