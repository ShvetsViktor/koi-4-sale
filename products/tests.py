from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductImage


class ProductCatalogueTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create test products once for the entire test class.
        """
        cls.available_product = Product.objects.create(
            name="Kohaku",
            variety="Kohaku",
            price=250.00,
            size=35,
            age=2,
            status=Product.ProductStatus.AVAILABLE,
        )

        cls.unavailable_product = Product.objects.create(
            name="Unavailable Sanke",
            variety="Sanke",
            price=300.00,
            size=40,
            age=3,
            status=Product.ProductStatus.UNAVAILABLE,
        )

    def test_catalogue_displays_product_from_database(self):
        """
        AC1: The catalogue displays koi stored in the database.
        """
        response = self.client.get(reverse("product_list"))

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

    def test_catalogue_displays_only_primary_image(self):
        """AC2: Only the primary product image appears in the catalogue."""

        primary_image = ProductImage.objects.create(
            product=self.available_product,
            image="products/kohaku_primary.jpg",
            is_primary=True,
        )

        secondary_image = ProductImage.objects.create(
            product=self.available_product,
            image="products/kohaku_secondary.jpg",
            is_primary=False,
        )

        response = self.client.get(reverse("product_list"))

        self.assertContains(
            response,
            f'src="{primary_image.image.url}"',
        )

        self.assertNotContains(
            response,
            f'src="{secondary_image.image.url}"',
        )


class ProductDetailTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name="Japanese Showa",
            variety="Showa Sanshoku",
            price=450.00,
            size=40,
            age=3,
            description="Japanese koi with black, red and white patterns.",
            status=Product.ProductStatus.AVAILABLE,
        )

    def test_product_detail_displays_product_information(self):
        """The detail page displays information about a specific koi."""
        response = self.client.get(
            reverse("product_detail", args=[self.product.pk])
        )
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.variety)
        self.assertContains(response, "450.00")
        self.assertContains(response, self.product.description)

    def test_nonexistent_product_returns_404(self):
        """Requesting a nonexistent product returns HTTP 404."""
        response = self.client.get(
            reverse("product_detail", args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_product_detail_displays_images(self):
        """The detail page displays all images belonging to the product."""

        primary_image = ProductImage.objects.create(
            product=self.product,
            image="products/showa_primary.jpg",
            is_primary=True,
        )

        secondary_image = ProductImage.objects.create(
            product=self.product,
            image="products/showa_secondary.jpg",
            is_primary=False,
        )

        response = self.client.get(
            reverse("product_detail", args=[self.product.pk])
        )

        self.assertContains(response, primary_image.image.url)
        self.assertContains(response, secondary_image.image.url)
