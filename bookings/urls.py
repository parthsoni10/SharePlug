from django.urls import path
from . import views

urlpatterns = [
    path('station/<int:station_id>/', views.booking_page, name='booking_page'),
    path('confirm/<int:slot_id>/', views.confirm_booking, name='confirm_booking'),
    path('detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
