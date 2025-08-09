# smart_electric_service/services/models.py

from django.db import models
from django.conf import settings

class Service(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255, blank=True)
    long_description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class, e.g., fas fa-bolt")
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.service.name} - {self.feature_text}"

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), on_delete=models.SET_NULL, null=True, blank=True, related_name='service_requests')

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    technician = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    technician_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    technician_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request #{self.id} - {self.service.name} ({self.customer_phone})"