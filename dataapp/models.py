from django.conf import settings
from django.db import models


class Journal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    cover = models.ImageField(upload_to='journal_covers/', blank=True, null=True)

    def __str__(self):
        return self.title


class TripBooking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trip_bookings",
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    destination = models.CharField(max_length=100)
    from_location = models.CharField(max_length=255, blank=True)
    to_location = models.CharField(max_length=255, blank=True)
    depart_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    adults = models.PositiveSmallIntegerField(default=1)
    children = models.PositiveSmallIntegerField(default=0)
    cabin = models.CharField(max_length=50, default="Economy")
    budget = models.PositiveIntegerField()
    accommodation = models.CharField(max_length=50)
    trip_type = models.CharField(max_length=50, blank=True)
    special_requests = models.TextField(blank=True)
    pref_direct = models.BooleanField(default=False)
    pref_window = models.BooleanField(default=False)
    pref_breakfast = models.BooleanField(default=False)
    pref_attractions = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=30, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.destination} ({self.get_status_display()})"

    @property
    def service_fee(self):
        return 500

    @property
    def taxes(self):
        return round(self.budget * 0.18)

    @property
    def total_amount(self):
        return self.budget + self.service_fee + self.taxes
