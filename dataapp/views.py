from datetime import datetime

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import JournalForm, TripPlanForm, UserRegistrationForm
from .models import Journal, TripBooking


def data(request):
    return render(request, "dataapp/mainpage.html")


def mainpage(request):
    return render(request, "dataapp/mainpage.html")


def menu(request):
    return render(request, "dataapp/menu.html")


def about(request):
    return render(request, "dataapp/aboutus.html")


def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("plan_trip")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("plan_trip")
        messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, "dataapp/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("plan_trip")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.get_username()}!")
            return redirect("plan_trip")
        messages.error(request, "Invalid username or password.")
    return render(request, "dataapp/login.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("data")


def contact(request):
    return render(request, "dataapp/contact.html")


def checkout(request):
    return render(request, "dataapp/checkout.html")


@login_required
def checkout_destination(request):
    destination = request.GET.get("destination") or request.POST.get("destination")
    price_param = request.GET.get("price") or request.POST.get("price")

    if not destination or not price_param:
        messages.info(request, "Please select a destination to continue.")
        return redirect("menu")

    try:
        package_price = int(price_param)
    except (TypeError, ValueError):
        messages.error(request, "We couldn't read that package price. Please choose a destination again.")
        return redirect("menu")

    service_fee = 500
    taxes = round(package_price * 0.18)
    pricing = {
        "package": package_price,
        "service_fee": service_fee,
        "taxes": taxes,
        "total": package_price + service_fee + taxes,
    }

    def parse_date_range(raw_value):
        if not raw_value:
            return None, None
        parts = [part.strip() for part in raw_value.split("to") if part.strip()]
        try:
            depart = datetime.strptime(parts[0], "%Y-%m-%d").date()
        except (ValueError, IndexError):
            depart = None
        try:
            return_date = datetime.strptime(parts[1], "%Y-%m-%d").date() if len(parts) > 1 else None
        except (ValueError, IndexError):
            return_date = None
        return depart, return_date

    form_data = {
        "full_name": (request.POST.get("full_name") or request.user.get_full_name() or request.user.get_username() or "").strip(),
        "email": (request.POST.get("email") or request.user.email or "").strip(),
        "phone": (request.POST.get("phone") or "").strip(),
        "dates": (request.POST.get("dates") or "").strip(),
        "travelers": request.POST.get("travelers") or "1",
        "payment_method": request.POST.get("payment_method") or "",
    }

    if request.method == "POST":
        errors = []
        if not form_data["full_name"]:
            errors.append("Please provide your full name.")
        if not form_data["email"]:
            errors.append("Please provide an email address.")
        if not form_data["phone"]:
            errors.append("Please provide a phone number.")
        if not form_data["payment_method"]:
            errors.append("Select a payment method to continue.")

        try:
            travelers_count = max(1, int(form_data["travelers"]))
        except ValueError:
            travelers_count = 1

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            depart_date, return_date = parse_date_range(form_data["dates"])
            booking = TripBooking.objects.create(
                user=request.user,
                full_name=form_data["full_name"],
                email=form_data["email"],
                phone=form_data["phone"],
                destination=destination,
                from_location="",
                to_location="",
                depart_date=depart_date,
                return_date=return_date,
                adults=travelers_count,
                children=0,
                cabin="Economy",
                budget=package_price,
                accommodation="Destination Package",
                trip_type="Leisure",
                special_requests="",
                payment_method=form_data["payment_method"],
                status=TripBooking.Status.CONFIRMED,
            )
            messages.success(request, "Your destination booking is confirmed!")
            return redirect("confirm", booking_id=booking.id)

    context = {
        "destination_name": destination,
        "package_price": package_price,
        "pricing": pricing,
        "form_data": form_data,
    }
    return render(request, "dataapp/checkout_destination.html", context)


@login_required
def plan_trip(request):
    initial = {
        "full_name": request.user.get_full_name() or request.user.get_username(),
        "email": request.user.email,
    }
    recent_bookings = TripBooking.objects.filter(user=request.user).order_by("-created_at")[:3]

    if request.method == "POST":
        form = TripPlanForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = TripBooking.Status.PENDING
            booking.save()
            request.session["pending_booking_id"] = booking.id
            messages.success(request, "Trip details saved. Please confirm your booking.")
            return redirect("checkout_plan")
        messages.error(request, "Please fix the errors in the form.")
    else:
        form = TripPlanForm(initial=initial)

    return render(
        request,
        "dataapp/plan_trip.html",
        {"form": form, "recent_bookings": recent_bookings},
    )


@login_required
def checkout_plan(request):
    booking_id = request.session.get("pending_booking_id") or request.GET.get("booking")
    if not booking_id:
        messages.info(request, "Please plan a trip first.")
        return redirect("plan_trip")

    booking = get_object_or_404(TripBooking, pk=booking_id, user=request.user)
    pricing = {
        "package": booking.budget,
        "service_fee": booking.service_fee,
        "taxes": booking.taxes,
        "total": booking.total_amount,
    }

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        if not payment_method:
            messages.error(request, "Please choose a payment method.")
        else:
            booking.payment_method = payment_method
            booking.status = TripBooking.Status.CONFIRMED
            booking.updated_at = timezone.now()
            booking.save()
            request.session.pop("pending_booking_id", None)
            messages.success(request, "Booking confirmed!")
            return redirect("confirm", booking_id=booking.id)

    return render(
        request,
        "dataapp/checkout_plan.html",
        {"booking": booking, "pricing": pricing},
    )


@login_required
def confirm(request, booking_id):
    booking = get_object_or_404(TripBooking, pk=booking_id, user=request.user)
    pricing = {
        "package": booking.budget,
        "service_fee": booking.service_fee,
        "taxes": booking.taxes,
        "total": booking.total_amount,
    }
    return render(
        request,
        "dataapp/confirm.html",
        {"booking": booking, "pricing": pricing},
    )


def create_journal(request):
    if request.method == "POST":
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            journal = form.save()
            messages.success(request, "Journal created successfully!")
            return redirect("travel_map", pk=journal.pk)
        else:
            messages.error(request, "There was an error saving your journal.")
    else:
        form = JournalForm()

    real_journals = list(Journal.objects.order_by("-date")[:6])

    class ExampleJournal:
        def __init__(self, title, location, date, cover_url, pk=None):
            self.title = title
            self.location = location
            self.date = date
            self.cover_url = cover_url
            self.pk = pk
            self.cover = type("obj", (object,), {"url": cover_url})()

    from datetime import date, timedelta

    example_journals = [
        ExampleJournal(
            title="Journey to Alaska",
            location="Alaska, USA",
            date=date.today() - timedelta(days=20),
            cover_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=400&q=80",
            pk=None,
        ),
    ]

    recent_journals = real_journals + example_journals[: max(0, 6 - len(real_journals))]

    return render(
        request,
        "dataapp/create_journal.html",
        {"form": form, "recent_journals": recent_journals},
    )


def travel_map(request, pk):
    journal = Journal.objects.get(pk=pk)
    return render(request, "dataapp/journel_detail.html", {"journal": journal})


@login_required
def my_bookings(request):
    bookings = TripBooking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "dataapp/my_bookings.html", {"bookings": bookings})


