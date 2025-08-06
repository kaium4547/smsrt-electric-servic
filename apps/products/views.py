# smart_electric_service/products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None):
    # For now, return the static products page
    return render(request, 'products.html')

def product_detail(request, id, slug):
    # For now, return the static products page
    return render(request, 'products.html')