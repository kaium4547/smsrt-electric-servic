from django.urls import path
from . import views

app_name = 'location'

urlpatterns = [
    path('api/divisions/', views.get_divisions, name='get_divisions'),
    path('api/districts/', views.get_districts, name='get_districts'),
    path('api/upazilas/', views.get_upazilas, name='get_upazilas'),
    path('api/unions/', views.get_unions, name='get_unions'),
    path('api/villages/', views.get_villages, name='get_villages'),
]

