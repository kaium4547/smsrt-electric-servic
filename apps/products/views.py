# smart_electric_service/products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Category, Product
from orders.models import Order, OrderItem


def product_list(request, category_slug=None):
	category = None
	categories = Category.objects.all().order_by('name')
	products = Product.objects.filter(available=True).select_related('category').order_by('-created') if hasattr(Product, 'created') else Product.objects.filter(available=True).select_related('category')
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	context = {
		"category": category,
		"categories": categories,
		"products": products,
	}
	return render(request, 'products/product_list.html', context)


def product_detail(request, id, slug):
	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	return render(request, 'products/product_detail.html', {"product": product})


def buy_now(request, id, slug):
	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	if request.method == 'POST':
		full_name = request.POST.get('full_name', '').strip()
		phone = request.POST.get('phone', '').strip()
		email = request.POST.get('email', '').strip() or None
		address = request.POST.get('address', '').strip()
		quantity_raw = request.POST.get('quantity', '1').strip()
		try:
			quantity = max(1, int(quantity_raw))
		except ValueError:
			quantity = 1

		if not full_name or not phone or not address:
			messages.error(request, 'অনুগ্রহ করে নাম, ফোন এবং ঠিকানা প্রদান করুন।')
			return render(request, 'products/buy_now.html', {"product": product})

		order = Order.objects.create(
			user=None,
			first_name=full_name.split(' ')[0],
			last_name=' '.join(full_name.split(' ')[1:]) or '',
			email=email or '',
			phone=phone,
			address=address,
		)
		OrderItem.objects.create(
			order=order,
			product=product,
			price=product.price,
			quantity=quantity,
		)
		messages.success(request, 'আপনার অর্ডার গ্রহণ করা হয়েছে। শীঘ্রই যোগাযোগ করা হবে।')
		return redirect(reverse('products:product_detail', args=[product.id, product.slug]))

	return render(request, 'products/buy_now.html', {"product": product})