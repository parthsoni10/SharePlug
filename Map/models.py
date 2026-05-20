from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EVStation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    num_chargers = models.IntegerField(null=True, blank=True, default=1)
    charger_types = models.CharField(max_length=200, blank=True)
    availability_status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)  # admin can deactivate

    image = models.ImageField(
        upload_to="stations/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Linked to business registration (set when approved)
    owner = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='owned_stations'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def total_bookings(self):
        return self.bookings.count()


class Vehicle(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Vehicle ({self.id})"


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(EVStation, on_delete=models.CASCADE, related_name='checkins')
    checkin_time = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} @ {self.station.name}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(EVStation, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "station")

    def __str__(self):
        return f"{self.user.username} → {self.station.name}"


class EVStationImage(models.Model):
    station = models.ForeignKey(
        EVStation,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="stations/gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.station.name} image"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(EVStation, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'station')

    def __str__(self):
        return f"{self.user.username} rated {self.station.name} {self.rating}★"


# ─── Business Models ──────────────────────────────────────────────────────────

class BusinessProfile(models.Model):
    BUSINESS_TYPES = [
        ('individual', 'Individual'),
        ('company', 'Company / Organization'),
        ('government', 'Government Entity'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPES, default='individual')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gst_number = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class StationRegistration(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='station_registrations')
    station = models.OneToOneField(
        EVStation, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='registration'
    )

    # Station details stored during registration
    station_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)

    # Documents
    license_doc = models.FileField(upload_to='business/docs/', null=True, blank=True)
    station_image = models.ImageField(upload_to='business/images/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='reviewed_registrations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.station_name} ({self.get_status_display()})"


class ChargerDetail(models.Model):
    CHARGER_TYPES = [
        ('Type1', 'Type 1 (J1772)'),
        ('Type2', 'Type 2 (Mennekes)'),
        ('CCS1', 'CCS Combo 1'),
        ('CCS2', 'CCS Combo 2'),
        ('CHAdeMO', 'CHAdeMO'),
        ('GB/T', 'GB/T (China Standard)'),
        ('Tesla', 'Tesla Supercharger'),
    ]
    registration = models.ForeignKey(StationRegistration, on_delete=models.CASCADE, related_name='chargers')
    charger_type = models.CharField(max_length=20, choices=CHARGER_TYPES)
    power_kw = models.FloatField(help_text="Power in kilowatts")
    connector_count = models.IntegerField(default=1)
    price_per_kwh = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.charger_type} {self.power_kw}kW x{self.connector_count}"


# ─── Booking Models ───────────────────────────────────────────────────────────

class TimeSlot(models.Model):
    station = models.ForeignKey(EVStation, on_delete=models.CASCADE, related_name='time_slots')
    charger_type = models.CharField(max_length=50)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ('station', 'charger_type', 'date', 'start_time')

    def __str__(self):
        return f"{self.station.name} | {self.charger_type} | {self.date} {self.start_time}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='bookings')
    station = models.ForeignKey(EVStation, on_delete=models.CASCADE, related_name='bookings')
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} @ {self.station.name}"
