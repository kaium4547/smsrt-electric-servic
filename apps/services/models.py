# smart_electric_service/services/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _

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

class ServiceBooking(models.Model):
    class PreferredTimeOfDay(models.TextChoices):
        MORNING = "morning", _("সকাল")
        AFTERNOON = "afternoon", _("দুপুর")
        EVENING = "evening", _("সন্ধ্যা")

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255)
    preferred_date = models.DateField(blank=True, null=True)
    preferred_time = models.CharField(max_length=20, choices=PreferredTimeOfDay.choices, blank=True)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.service.name}"