# smart_electric_service/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

SERVICE_CATEGORIES = (
    ('electrical', 'ইলেকট্রিক্যাল কাজ'),
    ('solar', 'সোলার সলিউশন'),
    ('cctv', 'সিসিটিভি/সিকিউরিটি'),
    ('ac', 'এসি সার্ভিস'),
    ('ips', 'আইপিএস/পাওয়ার ব্যাকআপ'),
    ('fridge', 'রেফ্রিজারেটর/অ্যাপ্লায়েন্স'),
    ('plumbing', 'প্লাম্বিং/পাইপিং'),
    ('other', 'অন্যান্য'),
)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'কাস্টমার'),
        ('technician', 'টেকনিশিয়ান'),
    )
    
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer', verbose_name='ইউজার টাইপ')
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

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

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES, default='other')
    subject = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f"ContactMessage({self.name}, {self.email})"

class SupportChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES, default='other')
    message = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self) -> str:
        return f"SupportChatMessage({self.name or (self.user and self.user.username) or 'guest'})"