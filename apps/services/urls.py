# smart_electric_service/services/urls.py

from django.urls import path
from . import views

app_name = 'services' # namespace for services app

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:id>/<slug:slug>/', views.service_detail, name='service_detail'),
]