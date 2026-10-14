from django.urls import path
from .views import ReservationCreate

urlpatterns = [
    path("reserve/", ReservationCreate.as_view(), name="reservation_create"),
]
