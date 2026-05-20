from django.urls import path
from . import views

urlpatterns = [
    path('', views.business_landing, name='business_landing'),
    path('profile/', views.business_profile_setup, name='business_profile_setup'),
    path('register-station/', views.station_register, name='station_register'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('dashboard/', views.business_dashboard, name='business_dashboard'),
]
