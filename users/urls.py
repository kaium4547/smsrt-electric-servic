# smart_electric_service/users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    # Tracking endpoints
    path('technician/tracking/toggle/', views.toggle_tracking, name='toggle_tracking'),
    path('technician/tracking/update/', views.update_tracking_location, name='update_tracking_location'),
    path('technicians/map/', views.technicians_map, name='technicians_map'),
    path('live-map/', views.live_map, name='live_map'),
]