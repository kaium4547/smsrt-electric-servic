# smart_electric_service/services/admin.py

from django.contrib import admin
from .models import Service, ServiceFeature, ServiceRequest

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'available', 'created', 'updated']
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceFeatureInline]

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['service', 'feature_text']
    list_filter = ['service']

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'customer_name', 'customer_phone', 'status', 'technician', 'created']
    list_filter = ['status', 'service', 'technician']
    search_fields = ['customer_name', 'customer_phone', 'customer_email', 'address']