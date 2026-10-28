from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from cloudinary import CloudinaryImage
from django.db import IntegrityError, transaction
from django.contrib.staticfiles.storage import staticfiles_storage

from .models import Product, ProductImage, Category


class Custom404PageTests(TestCase):
    """Test the custom page-not-found response."""

    @override_settings(DEBUG=False)
    def test_unknown_url_displays_custom_404_page(self):
        """Unknown URLs return the custom 404 page."""

        response = self.client.get("/non-existent-page/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Page Not Found", status_code=404)
        self.assertContains(response, "Back to Home", status_code=404)


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
                "images-TOTAL_FORMS": "0",
                "images-INITIAL_FORMS": "0",
                "images-MIN_NUM_FORMS": "0",
                "images-MAX_NUM_FORMS": "1000",
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
            image=CloudinaryImage("products/kohaku_primary"),
            is_primary=True,
        )

        secondary_image = ProductImage.objects.create(
            product=self.available_product,
            image=CloudinaryImage("products/kohaku_secondary"),
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

    def test_catalogue_displays_fallback_image(self):
        """Display a placeholder when a product has no primary image."""

        response = self.client.get(reverse("product_list"))

        self.assertContains(
            response,
            staticfiles_storage.url("images/default.png"),
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
            image=CloudinaryImage("products/showa_primary"),
            is_primary=True,
        )

        secondary_image = ProductImage.objects.create(
            product=self.product,
            image=CloudinaryImage("products/showa_secondary"),
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

    def test_product_detail_displays_breadcrumbs(self):
        """Display navigation breadcrumbs on the product detail page."""
        response = self.client.get(
            reverse("product_detail", args=[self.product.pk])
        )

        self.assertContains(
            response,
            '<nav class="breadcrumbs" aria-label="Breadcrumb">'
        )
        self.assertContains(response, "Home")
        self.assertContains(response, "Catalogue")
        self.assertContains(response, self.product.name)


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
        """All available products are displayed
        when no category is selected."""

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

    def test_invalid_category_id_returns_404(self):
        """Return HTTP 404 for a non-numeric category ID."""

        response = self.client.get(
            reverse("product_list"),
            {"category": "abc"},
        )

        self.assertEqual(response.status_code, 404)

    def test_nonexistent_category_id_returns_404(self):
        """Return HTTP 404 for a category that does not exist."""

        response = self.client.get(
            reverse("product_list"),
            {"category": 99999},
        )

        self.assertEqual(response.status_code, 404)


class ProductSearchTests(TestCase):
    """Tests for searching available koi by name or category."""

    @classmethod
    def setUpTestData(cls):
        cls.kohaku = Category.objects.create(name="Kohaku")
        cls.showa = Category.objects.create(name="Showa")

        cls.product_kohaku = Product.objects.create(
            name="Japanese Kohaku",
            category=cls.kohaku,
            price=250.00,
            size=35,
            age=2,
        )

        cls.product_showa = Product.objects.create(
            name="Japanese Showa",
            category=cls.showa,
            price=350.00,
            size=40,
            age=3,
        )

        cls.reserved_product = Product.objects.create(
            name="Premium Kohaku",
            category=cls.kohaku,
            price=500.00,
            size=45,
            age=4,
            status=Product.ProductStatus.RESERVED,
        )

    def test_search_by_product_name(self):
        """Search returns available products matching their name."""
        response = self.client.get(
            reverse("product_list"),
            {"q": "Japanese Showa"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["products"],
            [self.product_showa],
        )

    def test_search_by_category_name(self):
        """Search returns available products matching their category."""
        response = self.client.get(
            reverse("product_list"),
            {"q": "Kohaku"},
        )

        self.assertQuerySetEqual(
            response.context["products"],
            [self.product_kohaku],
        )

    def test_search_excludes_unavailable_products(self):
        """Reserved products are excluded from search results."""
        response = self.client.get(
            reverse("product_list"),
            {"q": "Premium Kohaku"},
        )

        self.assertQuerySetEqual(
            response.context["products"],
            [],
        )

    def test_search_no_results(self):
        """Search displays a message when no products match."""
        response = self.client.get(
            reverse("product_list"),
            {"q": "Nonexistent Koi"},
        )

        self.assertContains(
            response,
            "No koi found",
        )


class HomePageTests(TestCase):
    """Test the homepage."""

    def test_homepage_displays_hero_section(self):
        """The homepage displays a hero section with a catalogue link."""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Beautiful Koi, Raised with Care"
        )
        self.assertContains(
            response,
            f'href="{reverse("product_list")}"',
        )

    def test_homepage_header_links_to_home(self):
        """The site logo links to the homepage."""
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            'class="navbar-brand" href="/" aria-label="Koi4Sale home"'
        )
        self.assertContains(response, 'alt="Koi4Sale"')


class ProductPrimaryImageTests(TestCase):
    """Test primary product image selection and constraints."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Kohaku")
        cls.product = Product.objects.create(
            name="Japanese Kohaku",
            category=cls.category,
            price=250.00,
            size=35,
            age=2,
        )

    def test_primary_image_property(self):
        """Return the primary image or None when it is missing."""

        self.assertIsNone(self.product.primary_image)

        ProductImage.objects.create(
            product=self.product,
            image="products/secondary",
            is_primary=False,
        )

        self.assertIsNone(self.product.primary_image)

        primary = ProductImage.objects.create(
            product=self.product,
            image="products/primary",
            is_primary=True,
        )

        self.assertEqual(self.product.primary_image, primary)

    def test_only_one_primary_image_per_product(self):
        """Prevent multiple primary images for the same product."""

        ProductImage.objects.create(
            product=self.product,
            image="products/primary",
            is_primary=True,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProductImage.objects.create(
                    product=self.product,
                    image="products/another_primary",
                    is_primary=True,
                )
