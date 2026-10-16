"""Tests for the shared navigation header."""

from django.test import TestCase
from django.urls import reverse


class HeaderTemplateTests(TestCase):
    """Verify the navigation structure and responsive behaviour."""

    def test_navigation_links(self):
        """Header should contain links to the main pages."""
        response = self.client.get(reverse("home"))

        for url_name in ("home", "product_list", "cart"):
            with self.subTest(url_name=url_name):
                self.assertContains(
                    response,
                    f'href="{reverse(url_name)}"',
                )

    def test_responsive_navbar(self):
        """Navbar should use Bootstrap's large-screen breakpoint."""
        response = self.client.get(reverse("home"))

        self.assertContains(response, "navbar-expand-lg")
        self.assertContains(response, 'aria-label="Main navigation"')

    def test_mobile_navigation_toggle(self):
        """Mobile toggle should target the collapsible navigation."""
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'data-bs-toggle="collapse"')
        self.assertContains(response, 'data-bs-target="#mainNavbar"')
        self.assertContains(response, 'id="mainNavbar"')
        self.assertContains(response, 'aria-controls="mainNavbar"')

    def test_active_navigation_link(self):
        """Current page should have active styling and ARIA state."""
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            'class="nav-link active"',
        )
        self.assertContains(
            response,
            'aria-current="page"',
        )
