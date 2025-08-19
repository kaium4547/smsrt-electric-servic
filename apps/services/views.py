# smart_electric_service/services/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Service, ServiceBooking


def service_list(request):
	services = Service.objects.filter(available=True).order_by("name")
	return render(request, 'services/service_list.html', {"services": services})


def service_detail(request, id, slug):
	service = get_object_or_404(Service, id=id, slug=slug, available=True)
	return render(request, 'services/service_detail.html', {"service": service})


def service_book(request, id, slug):
	service = get_object_or_404(Service, id=id, slug=slug, available=True)
	if request.method == "POST":
		full_name = request.POST.get("full_name", "").strip()
		phone = request.POST.get("phone", "").strip()
		email = request.POST.get("email", "").strip() or None
		address = request.POST.get("address", "").strip()
		preferred_date = request.POST.get("preferred_date") or None
		preferred_time = request.POST.get("preferred_time", "").strip()
		message_text = request.POST.get("message", "").strip()

		if not full_name or not phone or not address:
			messages.error(request, "অনুগ্রহ করে নাম, ফোন এবং ঠিকানা প্রদান করুন।")
			return render(request, 'services/service_book.html', {"service": service})

		booking = ServiceBooking.objects.create(
			service=service,
			full_name=full_name,
			phone=phone,
			email=email,
			address=address,
			preferred_date=preferred_date if preferred_date else None,
			preferred_time=preferred_time,
			message=message_text,
		)
		messages.success(request, "আপনার বুকিং অনুরোধ গ্রহণ করা হয়েছে। আমরা শীঘ্রই যোগাযোগ করব।")
		return redirect(reverse('services:service_detail', args=[service.id, service.slug]))

	return render(request, 'services/service_book.html', {"service": service})