# smart_electric_service/services/admin.py

from django.contrib import admin
from .models import Service, ServiceFeature, ServiceCategory, ServiceSubcategory

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'subcategory', 'available', 'created', 'updated']
    list_filter = ['available', 'category', 'subcategory']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceFeatureInline]

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['service', 'feature_text']
    list_filter = ['service']

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ServiceSubcategory)
class ServiceSubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('name',)}