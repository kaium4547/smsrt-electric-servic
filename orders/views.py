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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        snap_lat = request.POST.get('snapshot_latitude')
        snap_lng = request.POST.get('snapshot_longitude')
        try:
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                snapshot_latitude=float(snap_lat) if snap_lat else None,
                snapshot_longitude=float(snap_lng) if snap_lng else None,
            )
            messages.success(request, 'Order created successfully!')
            return redirect('orders:order_detail', order_id=order.id)
        except Exception as e:
            messages.error(request, f'Order failed: {e}')
    
    products = Product.objects.filter(available=True)
    return render(request, 'orders/order_create.html', {'products': products}) 