from django import forms
import re

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

    def clean_phone(self):
        """Validate phone number format and length."""
        phone = self.cleaned_data["phone"].strip()

        if not re.fullmatch(r"\+?[0-9 ]+", phone):
            raise forms.ValidationError(
                "Enter a valid phone number using digits, spaces, "
                "and an optional leading +."
            )

        digits = re.sub(r"\D", "", phone)

        if not 7 <= len(digits) <= 15:
            raise forms.ValidationError(
                "Phone number must contain between 7 and 15 digits."
            )

        return phone
