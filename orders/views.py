from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from decimal import Decimal, InvalidOperation
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


@csrf_exempt  # Note: remove after serving checkout via Django template with {% csrf_token %}
@require_POST
def api_product_order(request):
    """Create Order and OrderItems from checkout payload"""
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    required_fields = ['firstName', 'lastName', 'email', 'phone', 'address', 'payment_method', 'cart']
    if not all(field in payload for field in required_fields):
        return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

    # Optional
    transaction_id = payload.get('transaction_id')
    notes = payload.get('notes')

    # Create Order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        first_name=payload['firstName'],
        last_name=payload['lastName'],
        email=payload['email'],
        phone=payload['phone'],
        address=payload['address'],
    )

    # Optional location fields
    division_id = payload.get('division')
    district_id = payload.get('district')
    upazila_id = payload.get('upazila')
    union_id = payload.get('union')
    village_id = payload.get('village')

    changed = False
    if division_id:
        order.division_id = division_id; changed = True
    if district_id:
        order.district_id = district_id; changed = True
    if upazila_id:
        order.upazila_id = upazila_id; changed = True
    if union_id:
        order.union_id = union_id; changed = True
    if village_id:
        order.village_id = village_id; changed = True
    if changed:
        order.save(update_fields=['division', 'district', 'upazila', 'union', 'village'])

    cart_items = payload.get('cart', [])
    if not isinstance(cart_items, list) or len(cart_items) == 0:
        return JsonResponse({'success': False, 'message': 'Cart cannot be empty'}, status=400)

    created_items = 0
    for item in cart_items:
        name = item.get('name')
        price = item.get('price')
        quantity = item.get('quantity', 1)
        slug = item.get('slug')

        product = None
        if slug:
            product = Product.objects.filter(slug=slug).first()
        if product is None and name:
            product = Product.objects.filter(name=name).first()

        try:
            price_dec = Decimal(str(price))
        except (InvalidOperation, TypeError):
            return JsonResponse({'success': False, 'message': f'Invalid price for item: {name}'}, status=400)

        try:
            qty_int = int(quantity)
            if qty_int <= 0:
                raise ValueError()
        except Exception:
            return JsonResponse({'success': False, 'message': f'Invalid quantity for item: {name}'}, status=400)

        OrderItem.objects.create(
            order=order,
            product=product,
            price=price_dec,
            quantity=qty_int
        )
        created_items += 1

    return JsonResponse({
        'success': True,
        'message': 'অর্ডার সফলভাবে সম্পন্ন হয়েছে',
        'order_id': order.id,
        'items_created': created_items
    })


@ensure_csrf_cookie
def checkout_page(request):
    """Render checkout page template with CSRF cookie"""
    return render(request, 'checkout.html')