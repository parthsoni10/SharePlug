from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from Map.models import (
    EVStation, StationRegistration, Booking,
    CheckIn, Review, BusinessProfile
)


def admin_required(view_func):
    """Decorator: staff members only."""
    return staff_member_required(view_func, login_url='/login/')


@admin_required
def dashboard(request):
    total_stations = EVStation.objects.filter(is_active=True).count()
    total_users = User.objects.filter(is_active=True).count()
    pending_regs = StationRegistration.objects.filter(status='pending').count()
    total_bookings = Booking.objects.count()
    total_checkins = CheckIn.objects.count()
    recent_regs = StationRegistration.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'admin_panel/dashboard.html', {
        'page': 'Admin Dashboard – SharePlug',
        'total_stations': total_stations,
        'total_users': total_users,
        'pending_regs': pending_regs,
        'total_bookings': total_bookings,
        'total_checkins': total_checkins,
        'recent_regs': recent_regs,
        'recent_users': recent_users,
    })


@admin_required
def registrations_list(request):
    status_filter = request.GET.get('status', 'pending')
    regs = StationRegistration.objects.filter(
        status=status_filter
    ).select_related('owner').prefetch_related('chargers').order_by('-submitted_at')

    return render(request, 'admin_panel/registrations.html', {
        'page': 'Station Registrations – Admin',
        'registrations': regs,
        'status_filter': status_filter,
        'counts': {
            'pending': StationRegistration.objects.filter(status='pending').count(),
            'approved': StationRegistration.objects.filter(status='approved').count(),
            'rejected': StationRegistration.objects.filter(status='rejected').count(),
            'draft': StationRegistration.objects.filter(status='draft').count(),
        }
    })


@admin_required
def registration_detail(request, reg_id):
    reg = get_object_or_404(StationRegistration, id=reg_id)
    chargers = reg.chargers.all()
    return render(request, 'admin_panel/registration_detail.html', {
        'page': f'Review: {reg.station_name}',
        'reg': reg,
        'chargers': chargers,
    })


@admin_required
@require_POST
def approve_registration(request, reg_id):
    reg = get_object_or_404(StationRegistration, id=reg_id)
    if reg.status != 'pending':
        messages.error(request, 'Only pending registrations can be approved.')
        return redirect('admin_registrations')

    # Create the live EVStation
    charger_types_str = ', '.join(
        c.get_charger_type_display() for c in reg.chargers.all()
    )
    num_chargers = sum(c.connector_count for c in reg.chargers.all())

    station = EVStation.objects.create(
        name=reg.station_name,
        address=reg.address,
        city=reg.city,
        state=reg.state,
        latitude=reg.latitude or 20.5937,
        longitude=reg.longitude or 78.9629,
        num_chargers=num_chargers or 1,
        charger_types=charger_types_str or 'Type2',
        availability_status=True,
        is_active=True,
        owner=reg.owner,
        image=reg.station_image if reg.station_image else None,
    )

    reg.station = station
    reg.status = 'approved'
    reg.reviewed_at = timezone.now()
    reg.reviewed_by = request.user
    reg.save()

    messages.success(request, f'✅ Station "{reg.station_name}" approved and is now live on the map!')
    return redirect('admin_registrations')


@admin_required
@require_POST
def reject_registration(request, reg_id):
    reg = get_object_or_404(StationRegistration, id=reg_id)
    reason = request.POST.get('reason', '').strip()
    if not reason:
        messages.error(request, 'Please provide a rejection reason.')
        return redirect('admin_registration_detail', reg_id=reg_id)

    reg.status = 'rejected'
    reg.admin_notes = reason
    reg.reviewed_at = timezone.now()
    reg.reviewed_by = request.user
    reg.save()

    messages.success(request, f'Registration rejected. Owner has been notified.')
    return redirect('admin_registrations')


@admin_required
def stations_list(request):
    stations = EVStation.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/stations.html', {
        'page': 'Manage Stations – Admin',
        'stations': stations,
    })


@admin_required
@require_POST
def toggle_station(request, station_id):
    station = get_object_or_404(EVStation, id=station_id)
    station.is_active = not station.is_active
    station.save()
    return JsonResponse({'is_active': station.is_active})


@admin_required
def users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {
        'page': 'Manage Users – Admin',
        'users': users,
    })


@admin_required
def bookings_list(request):
    bookings = Booking.objects.select_related('user', 'station', 'time_slot').order_by('-booked_at')
    return render(request, 'admin_panel/bookings.html', {
        'page': 'All Bookings – Admin',
        'bookings': bookings,
    })


@admin_required
def analytics(request):
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    import json

    # Registrations over time (last 30 days)
    reg_data_raw = (
        StationRegistration.objects
        .filter(submitted_at__isnull=False)
        .annotate(day=TruncDate('submitted_at'))
        .values('day').annotate(count=Count('id'))
        .order_by('day')[:30]
    )
    
    # Safely convert date objects to string formats for JSON serialization
    reg_data = []
    for d in reg_data_raw:
        if d['day']:
            day_str = d['day'].strftime('%Y-%m-%d')
        else:
            day_str = ''
        reg_data.append({'day': day_str, 'count': d['count']})

    # Stations by state
    state_data_raw = (
        EVStation.objects.filter(is_active=True)
        .values('state').annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    state_data = list(state_data_raw)

    return render(request, 'admin_panel/analytics.html', {
        'page': 'Analytics – Admin',
        'reg_data': json.dumps(reg_data),
        'state_data': json.dumps(state_data),
        'total_stations': EVStation.objects.filter(is_active=True).count(),
        'total_users': User.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_checkins': CheckIn.objects.count(),
        'total_reviews': Review.objects.count(),
    })

