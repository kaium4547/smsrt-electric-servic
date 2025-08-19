# smart_electric_service/services/admin.py

from django.contrib import admin
from .models import Service, ServiceFeature, ServiceBooking

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'available', 'created', 'updated']
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceFeatureInline]
    search_fields = ("name", "short_description")

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['service', 'feature_text']
    list_filter = ['service']
    search_fields = ("service__name", "feature_text")

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ("service", "full_name", "phone", "preferred_date", "preferred_time", "created_at")
    list_filter = ("service", "preferred_time", "created_at")
    search_fields = ("full_name", "phone", "email", "address", "service__name")