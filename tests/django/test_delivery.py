"""Tests for the delivery information page."""

from django.test import TestCase
from django.urls import reverse


class DeliveryPageTests(TestCase):
    """Test the delivery information page."""

    def test_delivery_page_returns_success(self):
        """The delivery page should return HTTP 200."""
        response = self.client.get(reverse("delivery"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delivery.html")

    def test_delivery_page_displays_heading(self):
        """The delivery page should display its heading."""
        response = self.client.get(reverse("delivery"))

        self.assertContains(response, "Delivery Information")

    def test_delivery_page_displays_hero_image(self):
        """Delivery page should display its hero image."""
        response = self.client.get(reverse("delivery"))

        self.assertContains(response, 'alt="Delivery worker standing beside a van with packages"')
        self.assertContains(response, "/static/images/delivery.")

    def test_delivery_page_displays_delivery_steps(self):
        """Delivery page should display all four delivery steps."""
        response = self.client.get(reverse("delivery"))

        for heading in [
            "Order Confirmation",
            "Preparation",
            "Packing and Shipping",
            "Receiving Your Koi",
        ]:
            self.assertContains(response, heading)
