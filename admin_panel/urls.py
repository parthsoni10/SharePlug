from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('registrations/', views.registrations_list, name='admin_registrations'),
    path('registrations/<int:reg_id>/', views.registration_detail, name='admin_registration_detail'),
    path('registrations/<int:reg_id>/approve/', views.approve_registration, name='admin_approve'),
    path('registrations/<int:reg_id>/reject/', views.reject_registration, name='admin_reject'),
    path('stations/', views.stations_list, name='admin_stations'),
    path('stations/<int:station_id>/toggle/', views.toggle_station, name='admin_toggle_station'),
    path('users/', views.users_list, name='admin_users'),
    path('bookings/', views.bookings_list, name='admin_bookings'),
    path('analytics/', views.analytics, name='admin_analytics'),
]
