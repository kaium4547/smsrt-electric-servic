from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from apps.products.models import Product

@login_required
def order_list(request):
    """Show all orders for the current user"""
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """Show order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    """Create a new order"""
    if request.method == 'POST':
        # Handle order creation logic here
        messages.success(request, 'Order created successfully!')
        return redirect('orders:order_list')
    
    products = Product.objects.filter(available=True)
    return render(request, 'orders/order_create.html', {'products': products}) 