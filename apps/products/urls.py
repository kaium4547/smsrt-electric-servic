# smart_electric_service/products/urls.py

from django.urls import path
from . import views

app_name = 'products' # namespace for products app

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('showcase/', views.showcase_tailwind, name='showcase'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/buy/', views.buy_now, name='buy_now'),
]