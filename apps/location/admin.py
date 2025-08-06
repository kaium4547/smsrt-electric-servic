# smart_electric_service/location/admin.py

from django.contrib import admin
from .models import Division, District, Upazila, Union, Village

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'bn_name']
    search_fields = ['name', 'bn_name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'bn_name', 'division']
    list_filter = ['division']
    search_fields = ['name', 'bn_name']

@admin.register(Upazila)
class UpazilaAdmin(admin.ModelAdmin):
    list_display = ['name', 'bn_name', 'district']
    list_filter = ['district', 'district__division']
    search_fields = ['name', 'bn_name']

@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    list_display = ['name', 'bn_name', 'upazila']
    list_filter = ['upazila', 'upazila__district']
    search_fields = ['name', 'bn_name']

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ['name', 'bn_name', 'union']
    list_filter = ['union', 'union__upazila']
    search_fields = ['name', 'bn_name']