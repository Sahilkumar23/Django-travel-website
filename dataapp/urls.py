from django.urls import path

from . import views

urlpatterns = [
    path("", views.data, name="data"),
    path("data/", views.data),
    path("main/", views.mainpage, name="mainpage"),
    path("menu/", views.menu, name="menu"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("contact/", views.contact, name="contact"),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "checkout-destination/",
        views.checkout_destination,
        name="checkout_destination",
    ),
    path("checkout-plan/", views.checkout_plan, name="checkout_plan"),
    path("confirm/<int:booking_id>/", views.confirm, name="confirm"),
    path("map/<int:pk>/", views.travel_map, name="travel_map"),
    path("createjournal/", views.create_journal, name="create_journal"),
    path("plantrip/", views.plan_trip, name="plan_trip"),
    path("bookings/", views.my_bookings, name="my_bookings"),
]
