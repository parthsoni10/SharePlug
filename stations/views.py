import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from geopy.distance import geodesic
from Map.models import EVStation, CheckIn, Bookmark, EVStationImage, Review

# ─── HOME ─────────────────────────────────────────────────────────────────────
def home(request):
    """Render map page. Stations loaded dynamically via API."""
    return render(request, 'home.html', {'page': 'SharePlug – Find EV Charging Stations'})

# ─── MAP API ──────────────────────────────────────────────────────────────────
def stations_in_bounds(request):
    """
    Return stations within map viewport bounds.
    Query: ?sw_lat=&sw_lng=&ne_lat=&ne_lng=
    """
    try:
        sw_lat = float(request.GET.get('sw_lat', 8))
        sw_lng = float(request.GET.get('sw_lng', 68))
        ne_lat = float(request.GET.get('ne_lat', 37))
        ne_lng = float(request.GET.get('ne_lng', 97))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid bounds'}, status=400)

    stations = EVStation.objects.filter(
        is_active=True,
        latitude__gte=sw_lat, latitude__lte=ne_lat,
        longitude__gte=sw_lng, longitude__lte=ne_lng
    ).values(
        'id', 'name', 'latitude', 'longitude',
        'num_chargers', 'charger_types', 'availability_status',
        'city', 'state', 'address'
    )[:300]

    return JsonResponse({'stations': list(stations)})

def get_nearest_station(request):
    try:
        latitude = float(request.GET.get('latitude'))
        longitude = float(request.GET.get('longitude'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

    user_location = (latitude, longitude)
    stations = list(EVStation.objects.filter(is_active=True)[:500])

    if not stations:
        return JsonResponse({'error': 'No stations found'}, status=404)

    nearest = min(
        stations,
        key=lambda s: geodesic(user_location, (s.latitude, s.longitude)).km
    )
    distance = geodesic(user_location, (nearest.latitude, nearest.longitude)).km

    return JsonResponse({
        "id": nearest.id,
        "name": nearest.name,
        "coordinates": [nearest.latitude, nearest.longitude],
        "distance": round(distance, 2)
    })

def location_detail(request, station_id):
    station = get_object_or_404(EVStation, id=station_id, is_active=True)

    # Always return JSON for AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        image_url = ''
        if station.image:
            try:
                image_url = station.image.url
            except Exception:
                image_url = ''

        avg_rating = station.average_rating()
        reviews = list(station.reviews.select_related('user').order_by('-created_at')[:5].values(
            'user__username', 'rating', 'comment', 'created_at'
        ))

        bookmarked = False
        if request.user.is_authenticated:
            bookmarked = Bookmark.objects.filter(user=request.user, station=station).exists()

        return JsonResponse({
            "id": station.id,
            "name": station.name,
            "state": station.state,
            "city": station.city,
            "address": station.address,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "num_chargers": station.num_chargers,
            "charger_types": station.charger_types,
            "availability_status": station.availability_status,
            "image": image_url,
            "avg_rating": avg_rating,
            "reviews": reviews,
            "bookmarked": bookmarked,
            "total_checkins": station.checkins.count(),
        })

    # Regular page load — render home with selected station
    return render(request, "home.html", {
        "page": f"{station.name} – SharePlug",
        "selected_station_id": station.id
    })

# ─── CHECK-IN ─────────────────────────────────────────────────────────────────
@login_required(login_url='/login/')
def checkin_page(request, station_id):
    station = get_object_or_404(EVStation, id=station_id)
    already_checked = CheckIn.objects.filter(user=request.user, station=station).exists()

    if request.method == "POST" and not already_checked:
        note = request.POST.get("note", "")
        CheckIn.objects.create(user=request.user, station=station, note=note)
        messages.success(request, f"Checked in at {station.name} ✅")
        return redirect('checkin', station_id=station.id)

    return render(request, "checkin.html", {
        "page": f"Check In – {station.name}",
        "station": station,
        "already_checked": already_checked
    })

@login_required(login_url='/login/')
def checkin_list(request):
    checkins = CheckIn.objects.filter(
        user=request.user
    ).select_related("station").order_by("-checkin_time")
    return render(request, "checkin_list.html", {
        "page": "My Check-Ins – SharePlug",
        "checkins": checkins
    })

# ─── BOOKMARKS ────────────────────────────────────────────────────────────────
@login_required(login_url='/login/')
@require_POST
def toggle_bookmark(request, station_id):
    station = get_object_or_404(EVStation, id=station_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, station=station)
    if not created:
        bookmark.delete()
        return JsonResponse({"bookmarked": False})
    return JsonResponse({"bookmarked": True})

@login_required(login_url='/login/')
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("station").order_by('-created_at')
    return render(request, "bookmarks.html", {
        "page": "My Bookmarks – SharePlug",
        "bookmarks": bookmarks
    })

@login_required(login_url='/login/')
def delete_bookmark(request, id):
    Bookmark.objects.filter(id=id, user=request.user).delete()
    return redirect('bookmark_list')

# ─── IMAGES ───────────────────────────────────────────────────────────────────
@login_required(login_url='/login/')
def upload_station_image(request, station_id):
    if request.method == "POST":
        station = get_object_or_404(EVStation, id=station_id)
        image = request.FILES.get("image")
        if not image:
            return JsonResponse({"error": "No image provided"}, status=400)
        img_obj = EVStationImage.objects.create(
            station=station, image=image, uploaded_by=request.user
        )
        return JsonResponse({"success": True, "image_url": img_obj.image.url})
    return JsonResponse({"error": "Invalid request"}, status=400)

def station_images(request, station_id):
    station = get_object_or_404(EVStation, id=station_id)
    images = [img.image.url for img in station.images.all()]
    return JsonResponse({"images": images})

# ─── REVIEWS ──────────────────────────────────────────────────────────────────
@login_required(login_url='/login/')
@require_POST
def add_review(request, station_id):
    station = get_object_or_404(EVStation, id=station_id)
    try:
        rating = int(request.POST.get('rating', 0))
    except ValueError:
        return JsonResponse({'error': 'Invalid rating'}, status=400)

    if not 1 <= rating <= 5:
        return JsonResponse({'error': 'Rating must be 1–5'}, status=400)

    comment = request.POST.get('comment', '').strip()
    review, created = Review.objects.update_or_create(
        user=request.user, station=station,
        defaults={'rating': rating, 'comment': comment}
    )
    return JsonResponse({
        'success': True,
        'avg_rating': station.average_rating(),
        'username': request.user.username,
        'rating': rating,
        'comment': comment,
    })
