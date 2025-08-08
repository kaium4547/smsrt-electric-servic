# smart_electric_service/users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TechnicianTracking

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'address',)}),
    )
    list_display = UserAdmin.list_display + ('phone_number',)

@admin.register(TechnicianTracking)
class TechnicianTrackingAdmin(admin.ModelAdmin):
    list_display = ('technician', 'enabled', 'visible_to_all_customers', 'current_latitude', 'current_longitude', 'updated_at')
    list_filter = ('enabled', 'visible_to_all_customers')
    search_fields = ('technician__username', 'technician__email')