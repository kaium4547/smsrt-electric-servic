# smart_electric_service/services/models.py

from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class ServiceSubcategory(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=120)
    slug = models.SlugField()

    class Meta:
        unique_together = ('category', 'slug')
        verbose_name = "Service Subcategory"
        verbose_name_plural = "Service Subcategories"

    def __str__(self):
        return f"{self.category.name} / {self.name}"

class Service(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    subcategory = models.ForeignKey(ServiceSubcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    short_description = models.CharField(max_length=255, blank=True)
    long_description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class, e.g., fas fa-bolt")
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
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