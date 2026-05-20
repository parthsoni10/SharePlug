from django.contrib import admin
from .models import (
    EVStation, Vehicle, CheckIn, Bookmark,
    EVStationImage, Review, BusinessProfile,
    StationRegistration, ChargerDetail, TimeSlot, Booking
)


@admin.register(EVStation)
class EVStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'num_chargers', 'availability_status', 'is_active']
    list_filter = ['state', 'availability_status', 'is_active']
    search_fields = ['name', 'city', 'state', 'address']
    list_editable = ['availability_status', 'is_active']


@admin.register(StationRegistration)
class StationRegistrationAdmin(admin.ModelAdmin):
    list_display = ['station_name', 'owner', 'city', 'state', 'status', 'submitted_at']
    list_filter = ['status']
    search_fields = ['station_name', 'owner__username', 'city']
    readonly_fields = ['submitted_at', 'reviewed_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'station', 'vehicle_number', 'status', 'booked_at']
    list_filter = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'station', 'rating', 'created_at']
    list_filter = ['rating']


admin.site.register(Vehicle)
admin.site.register(CheckIn)
admin.site.register(Bookmark)
admin.site.register(EVStationImage)
admin.site.register(BusinessProfile)
admin.site.register(ChargerDetail)
admin.site.register(TimeSlot)
