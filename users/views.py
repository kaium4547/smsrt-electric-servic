from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

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