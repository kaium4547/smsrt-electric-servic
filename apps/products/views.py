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


def showcase_tailwind(request):
	categories = ['All', 'ইলেকট্রিক', 'সোলার', 'নিরাপত্তা', 'কুলিং', 'প্লাম্বিং']
	products = [
		{
			"title": "সার্কিট ব্রেকার",
			"desc": "উচ্চ মানের সার্কিট ব্রেকার, নিরাপত্তা নিশ্চিত করে",
			"price": 850.00,
			"old_price": 950.00,
			"category": "ইলেকট্রিক",
			"img": "https://picsum.photos/seed/cb/400/300"
		},
		{
			"title": "সুইচ বোর্ড",
			"desc": "আধুনিক ডিজাইনের সুইচ বোর্ড",
			"price": 650.00,
			"old_price": 800.00,
			"category": "ইলেকট্রিক",
			"img": "https://picsum.photos/seed/sb/400/300"
		},
		{
			"title": "ইলেকট্রিক ওয়্যার",
			"desc": "উচ্চ মানের কপার ওয়্যার",
			"price": 1200.00,
			"old_price": 1400.00,
			"category": "ইলেকট্রিক",
			"img": "https://picsum.photos/seed/wire/400/300"
		},
		{
			"title": "সোলার প্যানেল",
			"desc": "উচ্চ দক্ষতার সোলার প্যানেল",
			"price": 18500.00,
			"old_price": 19800.00,
			"category": "সোলার",
			"img": "https://picsum.photos/seed/solar/400/300"
		},
		{
			"title": "সিসিটিভি ক্যামেরা",
			"desc": "উন্নত নিরাপত্তা সমাধান",
			"price": 3200.00,
			"old_price": 3600.00,
			"category": "নিরাপত্তা",
			"img": "https://picsum.photos/seed/cctv/400/300"
		},
		{
			"title": "এসি ইনডোর ইউনিট",
			"desc": "শক্তি সাশ্রয়ী কুলিং",
			"price": 28500.00,
			"old_price": 30500.00,
			"category": "কুলিং",
			"img": "https://picsum.photos/seed/ac/400/300"
		},
		{
			"title": "পিভিসি পাইপ",
			"desc": "প্লাম্বিং কাজের জন্য টেকসই",
			"price": 220.00,
			"old_price": 260.00,
			"category": "প্লাম্বিং",
			"img": "https://picsum.photos/seed/pipe/400/300"
		},
		{
			"title": "ওয়াটার ট্যাপ",
			"desc": "রস্ট-ফ্রি আধুনিক ট্যাপ",
			"price": 850.00,
			"old_price": 980.00,
			"category": "প্লাম্বিং",
			"img": "https://picsum.photos/seed/tap/400/300"
		},
	]
	return render(request, 'products/showcase_tailwind.html', {"categories": categories, "products": products})