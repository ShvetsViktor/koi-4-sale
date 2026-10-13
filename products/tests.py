from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductCatalogueTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create test products once for the entire test class.
        """
        cls.available_product = Product.objects.create(
            name="Kohaku",
            price=250.00,
            status="available",
        )

        cls.unavailable_product = Product.objects.create(
            name="Unavailable Sanke",
            price=300.00,
            status="unavailable",
        )

    def test_catalogue_displays_product_from_database(self):
        """
        AC1: The catalogue displays koi stored in the database.
        """
        response = self.client.get(reverse("product_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.available_product.name)

    def test_catalogue_displays_required_product_details(self):
        """
        AC2: Each koi displays its image, name, price,
        and relevant details.
        """
        response = self.client.get(reverse("product_list"))

        self.assertContains(response, self.available_product.name)
        self.assertContains(response, "250.00")

        # Image and relevant-detail assertions will be added
        # once we finalise the corresponding model fields.

    def test_catalogue_excludes_unavailable_products(self):
        """
        AC3: Unavailable koi are excluded from the catalogue.
        """
        response = self.client.get(reverse("product_list"))

        self.assertContains(response, self.available_product.name)
        self.assertNotContains(response, self.unavailable_product.name)