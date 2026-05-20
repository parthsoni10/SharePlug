from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from Map.models import BusinessProfile, StationRegistration, ChargerDetail


@login_required(login_url='/login/')
def business_landing(request):
    """Landing page — choose to register new or view existing."""
    has_profile = hasattr(request.user, 'business_profile')
    registrations = StationRegistration.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'business/landing.html', {
        'page': 'Start Business – SharePlug',
        'has_profile': has_profile,
        'registrations': registrations,
    })


@login_required(login_url='/login/')
def business_profile_setup(request):
    """Step 1: Create/update business profile."""
    existing = getattr(request.user, 'business_profile', None)
    if request.method == 'POST':
        data = {
            'business_name': request.POST.get('business_name', '').strip(),
            'business_type': request.POST.get('business_type', 'individual'),
            'phone': request.POST.get('phone', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'gst_number': request.POST.get('gst_number', '').strip(),
            'pan_number': request.POST.get('pan_number', '').strip(),
        }
        if not data['business_name'] or not data['phone'] or not data['email']:
            messages.error(request, 'Please fill all required fields.')
            return redirect('business_profile_setup')

        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
            existing.save()
        else:
            BusinessProfile.objects.create(user=request.user, **data)

        messages.success(request, 'Business profile saved! Now add your station. ✅')
        return redirect('station_register')

    return render(request, 'business/profile_setup.html', {
        'page': 'Business Profile – SharePlug',
        'profile': existing,
    })


@login_required(login_url='/login/')
def station_register(request):
    """Step 2-5: Multi-step station registration form."""
    if not hasattr(request.user, 'business_profile'):
        messages.warning(request, 'Please complete your business profile first.')
        return redirect('business_profile_setup')

    if request.method == 'POST':
        # Collect all form data
        station_name = request.POST.get('station_name', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        description = request.POST.get('description', '').strip()

        try:
            latitude = float(request.POST.get('latitude', 0))
            longitude = float(request.POST.get('longitude', 0))
        except ValueError:
            messages.error(request, 'Invalid location coordinates. Please select on map.')
            return redirect('station_register')

        if not all([station_name, address, city, state]):
            messages.error(request, 'Please fill all required station fields.')
            return redirect('station_register')

        reg = StationRegistration.objects.create(
            owner=request.user,
            station_name=station_name,
            address=address,
            city=city,
            state=state,
            latitude=latitude,
            longitude=longitude,
            description=description,
            station_image=request.FILES.get('station_image'),
            license_doc=request.FILES.get('license_doc'),
            status='draft',
        )

        # Create charger details
        charger_types = request.POST.getlist('charger_type[]')
        powers = request.POST.getlist('power_kw[]')
        counts = request.POST.getlist('connector_count[]')
        prices = request.POST.getlist('price_per_kwh[]')

        for i, ct in enumerate(charger_types):
            if ct:
                ChargerDetail.objects.create(
                    registration=reg,
                    charger_type=ct,
                    power_kw=float(powers[i]) if i < len(powers) and powers[i] else 7.4,
                    connector_count=int(counts[i]) if i < len(counts) and counts[i] else 1,
                    price_per_kwh=float(prices[i]) if i < len(prices) and prices[i] else 0,
                )

        # Move to pending
        reg.status = 'pending'
        reg.submitted_at = timezone.now()
        reg.save()

        messages.success(request, '🎉 Station registration submitted! Admin will review within 24-48 hours.')
        return redirect('my_registrations')

    charger_type_choices = ChargerDetail.CHARGER_TYPES
    return render(request, 'business/station_register.html', {
        'page': 'Register Station – SharePlug',
        'charger_types': charger_type_choices,
    })


@login_required(login_url='/login/')
def my_registrations(request):
    registrations = StationRegistration.objects.filter(
        owner=request.user
    ).prefetch_related('chargers').order_by('-created_at')
    return render(request, 'business/my_registrations.html', {
        'page': 'My Registrations – SharePlug',
        'registrations': registrations,
    })


@login_required(login_url='/login/')
def business_dashboard(request):
    """Dashboard for business owners to manage their stations."""
    if not hasattr(request.user, 'business_profile'):
        return redirect('business_profile_setup')

    owned_stations = request.user.owned_stations.filter(is_active=True)
    registrations = StationRegistration.objects.filter(owner=request.user)

    total_bookings = sum(s.total_bookings() for s in owned_stations)
    pending_count = registrations.filter(status='pending').count()
    approved_count = registrations.filter(status='approved').count()

    return render(request, 'business/dashboard.html', {
        'page': 'Business Dashboard – SharePlug',
        'profile': request.user.business_profile,
        'owned_stations': owned_stations,
        'registrations': registrations,
        'total_bookings': total_bookings,
        'pending_count': pending_count,
        'approved_count': approved_count,
    })
