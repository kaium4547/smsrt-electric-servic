from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import CustomUser, TechnicianTracking, ContactMessage


def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'সফলভাবে লগইন হয়েছে!')
            return redirect('home')
        else:
            messages.error(request, 'ভুল ইউজারনেম বা পাসওয়ার্ড!')
    
    return render(request, 'login.html')


def user_signup(request):
    """User signup view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        user_type = request.POST.get('userType')
        
        # Validation
        if not all([name, email, phone, password, confirm_password, user_type]):
            messages.error(request, 'সব ফিল্ড পূরণ করুন!')
            return render(request, 'signup.html')
        
        if password != confirm_password:
            messages.error(request, 'পাসওয়ার্ড দুটি মিলছে না!')
            return render(request, 'signup.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'এই ইমেইল ইতিমধ্যে ব্যবহৃত হয়েছে!')
            return render(request, 'signup.html')
        
        # Create user
        try:
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name,
                phone=phone,
                user_type=user_type
            )
            messages.success(request, 'সফলভাবে সাইনআপ হয়েছে! এখন লগইন করুন।')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'সাইনআপে সমস্যা হয়েছে: {str(e)}')
    
    return render(request, 'signup.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        try:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone or None,
                subject=subject or None,
                message=message,
                latitude=float(lat) if lat else None,
                longitude=float(lng) if lng else None,
            )
            messages.success(request, 'আপনার বার্তা পেয়েছি! ধন্যবাদ।')
            return redirect('contact')
        except Exception as e:
            messages.error(request, f'বার্তা পাঠাতে সমস্যা: {e}')
    return render(request, 'contact.html')


@login_required
def toggle_tracking(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    if request.user.user_type != 'technician' and not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')

    tracking, _ = TechnicianTracking.objects.get_or_create(technician=request.user)

    # Admin can force toggle by passing ?enabled=true/false, otherwise technician toggles their own
    enabled_param = request.POST.get('enabled')
    if enabled_param is not None and request.user.is_staff:
        tracking.enabled = enabled_param.lower() == 'true'
    else:
        tracking.enabled = not tracking.enabled

    # Optional visibility flag controlled by admin
    visible_param = request.POST.get('visible_to_all_customers')
    if visible_param is not None and request.user.is_staff:
        tracking.visible_to_all_customers = visible_param.lower() == 'true'

    tracking.save()
    return JsonResponse({
        'enabled': tracking.enabled,
        'visible_to_all_customers': tracking.visible_to_all_customers,
    })


@login_required
def update_tracking_location(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    if request.user.user_type != 'technician':
        return HttpResponseBadRequest('Only technicians can update location')

    lat = request.POST.get('latitude')
    lng = request.POST.get('longitude')
    try:
        lat = float(lat)
        lng = float(lng)
    except (TypeError, ValueError):
        return HttpResponseBadRequest('Invalid coordinates')

    tracking, _ = TechnicianTracking.objects.get_or_create(technician=request.user)
    if not tracking.enabled:
        return HttpResponseBadRequest('Tracking is disabled')

    tracking.current_latitude = lat
    tracking.current_longitude = lng
    tracking.save()
    return JsonResponse({'ok': True, 'updated_at': tracking.updated_at})


def technicians_map(request):
    # Only show technicians per visibility and optional query string filter
    q = TechnicianTracking.objects.filter(enabled=True)
    if not request.user.is_authenticated or not getattr(request.user, 'is_authenticated', False):
        q = q.filter(visible_to_all_customers=True)

    techs = [
        {
            'username': t.technician.username,
            'name': t.technician.get_full_name() or t.technician.username,
            'lat': t.current_latitude,
            'lng': t.current_longitude,
            'updated_at': t.updated_at.isoformat() if t.updated_at else None,
        }
        for t in q if t.current_latitude is not None and t.current_longitude is not None
    ]
    return render(request, 'technicians_map.html', {'technicians': techs})


def live_map(request):
    # Combined customer + technician live map page
    return render(request, 'live_map.html') 