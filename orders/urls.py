from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    # API endpoint for checkout
    path('api/product-order/', views.api_product_order, name='api_product_order'),
    # Checkout page served via Django template (for CSRF etc.)
    path('checkout/', views.checkout_page, name='checkout'),
] 