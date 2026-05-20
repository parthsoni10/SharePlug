from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from Map.models import EVStation, TimeSlot, Booking
import datetime


@login_required(login_url='/login/')
def booking_page(request, station_id):
    station = get_object_or_404(EVStation, id=station_id, is_active=True)
    today = timezone.localdate()

    # Get available dates (next 7 days)
    available_dates = [today + datetime.timedelta(days=i) for i in range(7)]

    selected_date_str = request.GET.get('date', str(today))
    try:
        selected_date = datetime.date.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = today

    # Get available slots
    slots = TimeSlot.objects.filter(
        station=station,
        date=selected_date,
        is_available=True
    ).order_by('start_time')

    # Auto-create slots if none exist (default: every hour 6am-10pm)
    if not slots.exists():
        for hour in range(6, 22):
            TimeSlot.objects.get_or_create(
                station=station,
                charger_type=station.charger_types[:20] if station.charger_types else 'Type2',
                date=selected_date,
                start_time=datetime.time(hour, 0),
                end_time=datetime.time(hour + 1, 0),
                defaults={'is_available': True, 'price': 150}
            )
        slots = TimeSlot.objects.filter(
            station=station,
            date=selected_date,
            is_available=True
        ).order_by('start_time')

    return render(request, 'bookings/booking_page.html', {
        'page': f'Book – {station.name}',
        'station': station,
        'slots': slots,
        'selected_date': selected_date,
        'available_dates': available_dates,
    })


@login_required(login_url='/login/')
@require_POST
def confirm_booking(request, slot_id):
    slot = get_object_or_404(TimeSlot, id=slot_id, is_available=True)
    vehicle_number = request.POST.get('vehicle_number', '').strip().upper()
    vehicle_model = request.POST.get('vehicle_model', '').strip()

    if not vehicle_number:
        messages.error(request, 'Please enter your vehicle number.')
        return redirect('booking_page', station_id=slot.station.id)

    # Create booking
    booking = Booking.objects.create(
        user=request.user,
        time_slot=slot,
        station=slot.station,
        vehicle_number=vehicle_number,
        vehicle_model=vehicle_model,
        status='confirmed',
        estimated_cost=slot.price,
    )

    # Mark slot unavailable
    slot.is_available = False
    slot.save()

    messages.success(request, '🎉 Booking confirmed!')
    return redirect('booking_detail', booking_id=booking.id)


@login_required(login_url='/login/')
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'page': f'Booking #{booking.id} – SharePlug',
        'booking': booking,
    })


@login_required(login_url='/login/')
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('station', 'time_slot').order_by('-booked_at')
    return render(request, 'bookings/my_bookings.html', {
        'page': 'My Bookings – SharePlug',
        'bookings': bookings,
    })


@login_required(login_url='/login/')
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
        # Re-open the slot
        booking.time_slot.is_available = True
        booking.time_slot.save()
        messages.success(request, 'Booking cancelled.')
    return redirect('my_bookings')
