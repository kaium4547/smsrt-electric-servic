from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'user_type')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'user_type')}),
    )
    list_display = UserAdmin.list_display + ('phone_number', 'user_type')
    list_filter = UserAdmin.list_filter + ('user_type',)

# Admin Site Customization
admin.site.site_header = "Smart Electric Service Admin"
admin.site.site_title = "Smart Electric Service Admin Portal"
admin.site.index_title = "Welcome to Smart Electric Service Admin Portal"

# Group admin models by app
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'available', 'created', 'updated']
    list_filter = ['available', 'created']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created']
    list_filter = ['available', 'created', 'category']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'email', 'phone', 'paid', 'status', 'created']
    list_filter = ['paid', 'status', 'created']
    search_fields = ['id', 'first_name', 'email', 'phone']
    list_editable = ['status', 'paid']
    readonly_fields = ['created', 'updated']

# Register models from apps
from apps.services.models import Service, ServiceFeature
from apps.products.models import Category, Product
from apps.location.models import Division, District, Upazila, Union, Village
from orders.models import Order, OrderItem

# Services
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceFeature)

# Products
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

# Location
admin.site.register(Division)
admin.site.register(District)
admin.site.register(Upazila)
admin.site.register(Union)
admin.site.register(Village)

# Orders
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem) 