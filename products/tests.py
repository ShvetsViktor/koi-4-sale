from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Product, ProductImage, Category


class ProductAdminTests(TestCase):
    """Test product management through Django Admin."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Kohaku")

        cls.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpassword123",
        )

        cls.product = Product.objects.create(
            name="Japanese Kohaku",
            category=cls.category,
            price=250.00,
            size=35,
            age=2,
        )

    def test_anonymous_user_cannot_access_product_admin(self):
        """Anonymous visitors must be redirected to admin login."""

        response = self.client.get(
            reverse("admin:products_product_changelist")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_can_view_product_list(self):
        """Administrators can view existing product listings."""

        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse("admin:products_product_changelist")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_admin_can_create_product(self):
        """Administrators can create new koi listings."""

        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse("admin:products_product_add"),
            {
                "name": "Japanese Showa",
                "category": self.category.pk,
                "price": "350.00",
                "size": 40,
                "age": 3,
                "status": Product.ProductStatus.AVAILABLE,
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Product.objects.filter(
                name="Japanese Showa",
                category=self.category,
            ).exists()
        )

    def test_regular_user_cannot_access_product_admin(self):
        """Regular users cannot access product management."""

        regular_user = get_user_model().objects.create_user(
            username="regular_user",
            password="testpassword123",
        )

        self.client.force_login(regular_user)

        response = self.client.get(
            reverse("admin:products_product_changelist")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)


class ProductCatalogueTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create test categories and products once for the entire test class.
        """
        cls.kohaku_category = Category.objects.create(name="Kohaku")
        cls.sanke_category = Category.objects.create(name="Sanke")

        cls.available_product = Product.objects.create(
            name="Kohaku",
            category=cls.kohaku_category,
            price=250.00,
            size=35,
            age=2,
            status=Product.ProductStatus.AVAILABLE,
        )

        cls.unavailable_product = Product.objects.create(
            name="Unavailable Sanke",
            category=cls.sanke_category,
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

    def test_catalogue_links_to_product_detail(self):
        """Each product links to its detail page."""

        response = self.client.get(reverse("product_list"))

        product_url = reverse(
            "product_detail",
            args=[self.available_product.pk]
        )

        self.assertContains(
            response,
            f'href="{product_url}"'
        )


class ProductDetailTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.showa_category = Category.objects.create(name="Showa Sanshoku")

        cls.product = Product.objects.create(
            name="Japanese Showa",
            category=cls.showa_category,
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
        self.assertContains(response, self.product.category.name)
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

    def test_product_detail_displays_availability(self):
        """The detail page displays the koi's availability status."""

        response = self.client.get(
            reverse("product_detail", args=[self.product.pk])
        )

        self.assertContains(
            response,
            self.product.get_status_display()
        )


class CategoryModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Kohaku")

    def test_category_has_name(self):
        """A category stores the koi variety name."""
        self.assertEqual(self.category.name, "Kohaku")

    def test_product_belongs_to_category(self):
        """A product belongs to a category."""
        product = Product.objects.create(
            name="Japanese Kohaku",
            category=self.category,
            price=450.00,
            size=40,
            age=3,
        )

        self.assertEqual(product.category, self.category)


class ProductFilteringTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.kohaku_category = Category.objects.create(name="Kohaku")
        cls.showa_category = Category.objects.create(name="Showa")

        cls.kohaku = Product.objects.create(
            name="Japanese Kohaku",
            category=cls.kohaku_category,
            price=250.00,
            size=35,
            age=2,
            status=Product.ProductStatus.AVAILABLE,
        )

        cls.showa = Product.objects.create(
            name="Japanese Showa",
            category=cls.showa_category,
            price=350.00,
            size=40,
            age=3,
            status=Product.ProductStatus.AVAILABLE,
        )

    def test_catalogue_filters_products_by_category(self):
        """Only products from the selected category are displayed."""

        response = self.client.get(
            reverse("product_list"),
            {"category": self.kohaku_category.pk},
        )

        self.assertContains(response, self.kohaku.name)
        self.assertNotContains(response, self.showa.name)

    def test_catalogue_without_category_shows_all_available_products(self):
        """All available products are displayed when no category is selected."""

        response = self.client.get(reverse("product_list"))

        self.assertContains(response, self.kohaku.name)
        self.assertContains(response, self.showa.name)

    def test_catalogue_displays_category_filter_links(self):
        """Catalogue provides category filters and a reset link."""

        response = self.client.get(reverse("product_list"))

        self.assertContains(
            response,
            f'href="?category={self.kohaku_category.pk}"',
        )

        self.assertContains(
            response,
            f'href="?category={self.showa_category.pk}"',
        )

        self.assertContains(
            response,
            'href="/products/"',
        )

    def test_empty_category_displays_message(self):
        """Display a message when no available koi match the category."""

        empty_category = Category.objects.create(name="Tancho")

        response = self.client.get(
            reverse("product_list"),
            {"category": empty_category.pk},
        )

        self.assertContains(response, "No koi available in this category.")
        self.assertNotContains(response, self.kohaku.name)
        self.assertNotContains(response, self.showa.name)
