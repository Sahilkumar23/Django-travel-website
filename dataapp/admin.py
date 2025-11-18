from django.contrib import admin
from .models import Journal, TripBooking


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "date")
    search_fields = ("title", "location")


@admin.register(TripBooking)
class TripBookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "destination", "status", "created_at")
    list_filter = ("status", "destination", "created_at")
    search_fields = ("full_name", "email", "destination")