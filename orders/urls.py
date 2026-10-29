from django.urls import path

from .views import (
    ReservationCreate,
    ReservationConfirmation,
    CartView,
    CartProductsView,
)

urlpatterns = [
    path(
        "reserve/",
        ReservationCreate.as_view(),
        name="reservation_create",
    ),
    path(
        "reservation-confirmation/<uuid:access_token>/",
        ReservationConfirmation.as_view(),
        name="reservation_confirmation",
    ),
    path(
        "cart/",
        CartView.as_view(),
        name="cart",
    ),
    path(
        "cart/products/",
        CartProductsView.as_view(),
        name="cart_products",
    ),
]
