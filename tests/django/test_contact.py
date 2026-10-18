from django.test import TestCase
from django.urls import reverse


class ContactPageTests(TestCase):
    """Test the contact information page."""

    def test_contact_page_returns_success(self):
        """Contact page should return HTTP 200."""
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact.html")

    def test_contact_page_displays_heading(self):
        """Contact page should display its main heading."""
        response = self.client.get(reverse("contact"))

        self.assertContains(response, "Get in Touch")

    def test_contact_page_displays_email_link(self):
        """Contact page should provide an email contact link."""
        response = self.client.get(reverse("contact"))

        self.assertContains(response, 'href="mailto:')
        self.assertContains(response, "Send an Email")

    def test_contact_page_displays_contact_information(self):
        """Contact page should display contact information."""
        response = self.client.get(reverse("contact"))

        self.assertContains(response, "Contact Information")
        self.assertContains(response, "Get in Touch")
