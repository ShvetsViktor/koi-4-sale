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