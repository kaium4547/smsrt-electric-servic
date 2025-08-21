# smart_electric_service/services/views.py
from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory, ServiceSubcategory

def service_list(request):
    category_slug = request.GET.get('category')
    subcategory_slug = request.GET.get('subcategory')

    categories = ServiceCategory.objects.all().order_by('name')
    active_category = None
    active_subcategory = None
    subcategories = []

    qs = Service.objects.filter(available=True).select_related('category', 'subcategory')
    if category_slug:
        active_category = ServiceCategory.objects.filter(slug=category_slug).first()
        if active_category:
            qs = qs.filter(category=active_category)
            subcategories = ServiceSubcategory.objects.filter(category=active_category).order_by('name')
    if subcategory_slug and active_category:
        active_subcategory = ServiceSubcategory.objects.filter(category=active_category, slug=subcategory_slug).first()
        if active_subcategory:
            qs = qs.filter(subcategory=active_subcategory)

    services = qs.prefetch_related('features')
    return render(request, 'services/service_list.html', {
        'services': services,
        'categories': categories,
        'active_category': active_category,
        'subcategories': subcategories,
        'active_subcategory': active_subcategory,
    })

def service_detail(request, id, slug):
    service = get_object_or_404(Service, id=id, slug=slug, available=True)
    features = service.features.all()
    return render(request, 'services/service_detail.html', {'service': service, 'features': features})