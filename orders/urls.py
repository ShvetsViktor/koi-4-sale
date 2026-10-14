from django.urls import path
from .views import ReservationCreate, ReservationConfirmation

urlpatterns = [
    path(
        "reserve/",
        ReservationCreate.as_view(),
        name="reservation_create"
        ),
    path(
        "reservation-confirmation/<int:pk>/",
        ReservationConfirmation.as_view(),
        name="reservation_confirmation",
    ),
]
