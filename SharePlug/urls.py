from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (
    login_page, logout_page, register_page
)
from stations.views import (
    home, get_nearest_station, location_detail,
    checkin_page, checkin_list,
    toggle_bookmark, bookmark_list, delete_bookmark,
    upload_station_image, station_images,
    stations_in_bounds, add_review
)


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("map/", include("Map.urls")),
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),

    # Map API
    path("get-nearest-station/", get_nearest_station, name='get_nearest_station'),
    path("api/stations/", stations_in_bounds, name='stations_in_bounds'),
    path('location/<int:station_id>/', location_detail, name='location_detail'),

    # Checkins
    path("checkin/<int:station_id>/", checkin_page, name="checkin"),
    path("checkins/", checkin_list, name="checkin_list"),

    # Bookmarks
    path("bookmark/<int:station_id>/", toggle_bookmark, name="toggle_bookmark"),
    path("bookmarks/", bookmark_list, name="bookmark_list"),
    path("bookmark/delete/<int:id>/", delete_bookmark, name="delete_bookmark"),

    # Images & Reviews
    path("station/<int:station_id>/upload-image/", upload_station_image, name='upload_image'),
    path("station/<int:station_id>/images/", station_images, name='station_images'),
    path("station/<int:station_id>/review/", add_review, name='add_review'),

    # Business registration
    path('start-business/', include('business.urls')),

    # Booking system
    path('book/', include('bookings.urls')),

    # Admin panel
    path('admin-panel/', include('admin_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])