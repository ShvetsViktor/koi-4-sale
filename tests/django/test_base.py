"""Tests for the shared base template."""

from django.test import TestCase
from django.urls import reverse


class BaseTemplateTests(TestCase):
    """Verify that the base template loads required assets."""

    def test_bootstrap_css_is_loaded(self):
        """Bootstrap CSS should be included in the rendered HTML."""
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            "bootstrap@5.3.8/dist/css/bootstrap.min.css",
        )

    def test_bootstrap_javascript_is_loaded(self):
        """Bootstrap JavaScript should be included in the rendered HTML."""
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            "bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js",
        )

    def test_custom_stylesheet_is_loaded(self):
        """The custom stylesheet should be included in the rendered HTML."""
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            'href="/static/css/style.css"',
        )
