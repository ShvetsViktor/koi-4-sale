from django import forms

from .models import Order


class ReservationForm(forms.ModelForm):
    """Collect and validate customer contact details."""

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "email",
            "phone",
        ]
