# smart_electric_service/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'কাস্টমার'),
        ('technician', 'টেকনিশিয়ান'),
    )
    
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer', verbose_name='ইউজার টাইপ')
    
    # আপনি আপনার প্রয়োজন অনুযায়ী আরও ফিল্ড যোগ করতে পারেন

    # ensure that email is unique or phone_number is unique
    class Meta:
        verbose_name = "User" # এটি আপনার মডেলের একক নাম
        verbose_name_plural = "Users" # এটি আপনার মডেলের বহু নাম

    def __str__(self):
        return self.username

class TechnicianTracking(models.Model):
    technician = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tracking')
    enabled = models.BooleanField(default=False, help_text="Admin-controlled: allow technician location sharing")
    visible_to_all_customers = models.BooleanField(
        default=False,
        help_text="If enabled, any logged-in customer can view this technician's live location"
    )
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Tracking({self.technician.username}) - {'ON' if self.enabled else 'OFF'}"