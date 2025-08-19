from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('services/', include('apps.services.urls')),
    path('products/', include('apps.products.urls')),
    path('orders/', include('orders.urls')),
    path('location/', include('apps.location.urls')),
    path('reviews/', include('reviews.urls')),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('login/', user_views.user_login, name='login'),
    path('signup/', user_views.user_signup, name='signup'),
    path('customer-dashboard/', TemplateView.as_view(template_name='customer-dashboard.html'), name='customer_dashboard'),
    path('technician-dashboard/', TemplateView.as_view(template_name='technician-dashboard.html'), name='technician_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)