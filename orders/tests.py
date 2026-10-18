from decimal import Decimal

from django.contrib.admin.sites import AdminSite
from django.contrib.staticfiles.storage import staticfiles_storage
from django.test import TestCase
from django.urls import reverse
from cloudinary import CloudinaryImage

from products.models import Category, Product, ProductImage

from .admin import OrderAdmin
from .forms import ReservationForm
from .models import Order, OrderItem


class OrderModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Kohaku")

        self.product = Product.objects.create(
            name="Japanese Kohaku",
            category=self.category,
            price=Decimal("250.00"),
            size=30,
            age=2,
        )

        self.order = Order.objects.create(
            customer_name="John Smith",
            email="john@example.com",
            phone="07123456789",
            total_price=Decimal("250.00"),
        )

    def test_order_default_status_is_pending(self):
        """New reservation requests should have pending status."""
        self.assertEqual(
            self.order.status,
            Order.OrderStatus.PENDING,
        )

    def test_order_item_links_product_to_order(self):
        """An order item should reference its order and product."""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
        )

        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product)
        self.assertIn(item, self.order.items.all())

    def test_order_item_preserves_original_price(self):
        """Changing a product price should not change the reserved price."""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
        )

        self.product.price = Decimal("300.00")
        self.product.save()

        item.refresh_from_db()

        self.assertEqual(item.price, Decimal("250.00"))

    def test_order_can_contain_multiple_products(self):
        """A reservation should support multiple individual koi."""
        second_product = Product.objects.create(
            name="Japanese Showa",
            category=self.category,
            price=Decimal("350.00"),
            size=35,
            age=3,
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
        )

        OrderItem.objects.create(
            order=self.order,
            product=second_product,
            price=second_product.price,
        )

        self.assertEqual(self.order.items.count(), 2)


class ReservationFormTests(TestCase):
    """Tests for customer reservation form validation."""

    def setUp(self):
        self.valid_data = {
            "customer_name": "John Smith",
            "email": "john@example.com",
            "phone": "07123456789",
        }

    def test_form_accepts_valid_data(self):
        """The form should accept valid customer contact details."""
        form = ReservationForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_customer_name_is_required(self):
        """Customer name must not be empty."""
        data = self.valid_data.copy()
        data["customer_name"] = ""

        form = ReservationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("customer_name", form.errors)

    def test_email_is_required(self):
        """Email must not be empty."""
        data = self.valid_data.copy()
        data["email"] = ""

        form = ReservationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_email_must_be_valid(self):
        """The form should reject incorrectly formatted email addresses."""
        data = self.valid_data.copy()
        data["email"] = "invalid-email"

        form = ReservationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_phone_is_required(self):
        """Phone number must not be empty."""
        data = self.valid_data.copy()
        data["phone"] = ""

        form = ReservationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_internal_fields_are_excluded(self):
        """Customers must not control reservation status or total price."""
        form = ReservationForm()

        self.assertNotIn("status", form.fields)
        self.assertNotIn("total_price", form.fields)

    def test_phone_rejects_letters(self):
        """Phone numbers containing letters should be rejected."""

        form = ReservationForm(
            data={
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "abc123456",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_phone_accepts_valid_uk_number(self):
        """Accept a valid UK phone number."""
        form = ReservationForm(data={
            "customer_name": "John Smith",
            "email": "john@example.com",
            "phone": "07123456789",
        })

        self.assertTrue(form.is_valid())

    def test_phone_accepts_international_number(self):
        """Accept an international number with spaces and a leading +."""
        form = ReservationForm(data={
            "customer_name": "John Smith",
            "email": "john@example.com",
            "phone": "+44 7123 456789",
        })

        self.assertTrue(form.is_valid())

    def test_phone_rejects_short_number(self):
        """Reject phone numbers containing fewer than 7 digits."""
        form = ReservationForm(data={
            "customer_name": "John Smith",
            "email": "john@example.com",
            "phone": "123456",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_phone_rejects_long_number(self):
        """Reject phone numbers containing more than 15 digits."""
        form = ReservationForm(data={
            "customer_name": "John Smith",
            "email": "john@example.com",
            "phone": "1234567890123456",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_phone_rejects_special_characters(self):
        """Reject phone numbers containing special characters."""
        form = ReservationForm(data={
            "customer_name": "John Smith",
            "email": "john@example.com",
            "phone": "07123-456789",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)


class ReservationViewTests(TestCase):
    """Tests for the reservation submission workflow."""

    def setUp(self):
        self.category = Category.objects.create(name="Kohaku")

        self.product_one = Product.objects.create(
            name="Japanese Kohaku",
            category=self.category,
            price=Decimal("250.00"),
            size=30,
            age=2,
        )

        self.product_two = Product.objects.create(
            name="Japanese Showa",
            category=self.category,
            price=Decimal("350.00"),
            size=35,
            age=3,
        )

    def test_customer_can_reserve_multiple_products(self):
        """A valid request should reserve all selected koi."""
        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "07123456789",
                "product_ids": [
                    str(self.product_one.pk),
                    str(self.product_two.pk),
                ],
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()

        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.total_price, Decimal("600.00"))
        self.assertEqual(order.status, Order.OrderStatus.PENDING)

        self.product_one.refresh_from_db()
        self.product_two.refresh_from_db()

        self.assertEqual(
            self.product_one.status,
            Product.ProductStatus.RESERVED,
        )

        self.assertEqual(
            self.product_two.status,
            Product.ProductStatus.RESERVED,
        )

    def test_cannot_reserve_unavailable_product(self):
        """A reserved koi cannot be included in a new reservation."""

        self.product_one.status = Product.ProductStatus.RESERVED
        self.product_one.save()

        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "07123456789",
                "product_ids": [
                    str(self.product_one.pk),
                    str(self.product_two.pk),
                ],
            },
        )

        self.assertEqual(response.status_code, 400)

        # No order should be created.
        self.assertEqual(Order.objects.count(), 0)

        # The available product must remain available.
        self.product_two.refresh_from_db()

        self.assertEqual(
            self.product_two.status,
            Product.ProductStatus.AVAILABLE,
        )

    def test_cannot_reserve_same_product_twice(self):
        """A koi cannot be reserved by two separate requests."""

        reservation_data = {
            "customer_name": "John Smith",
            "email": "john@example.com",
            "phone": "07123456789",
            "product_ids": [str(self.product_one.pk)],
        }

        # First reservation should succeed.
        first_response = self.client.post(
            reverse("reservation_create"),
            reservation_data,
        )

        self.assertEqual(first_response.status_code, 302)

        # Second reservation should be rejected.
        second_response = self.client.post(
            reverse("reservation_create"),
            {
                **reservation_data,
                "customer_name": "Jane Smith",
                "email": "jane@example.com",
            },
        )

        self.assertEqual(second_response.status_code, 400)

        # Only the first reservation should exist.
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        self.product_one.refresh_from_db()

        self.assertEqual(
            self.product_one.status,
            Product.ProductStatus.RESERVED,
        )

    def test_reservation_rejects_invalid_product_ids(self):
        """Invalid product IDs must not create a reservation."""

        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "07123456789",
                "product_ids": ["abc", str(self.product_one.pk)],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

        self.product_one.refresh_from_db()

        self.assertEqual(
            self.product_one.status,
            Product.ProductStatus.AVAILABLE,
        )

    def test_reservation_rejects_empty_product_list(self):
        """A reservation must contain at least one koi."""
        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "07123456789",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_reservation_rejects_duplicate_product_ids(self):
        """The same koi cannot appear twice in one request."""
        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "07123456789",
                "product_ids": [
                    str(self.product_one.pk),
                    str(self.product_one.pk),
                ],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_reservation_rejects_nonexistent_product(self):
        """A reservation cannot include a nonexistent koi."""
        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "07123456789",
                "product_ids": [
                    str(self.product_one.pk),
                    "999999",
                ],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_reservation_rejects_invalid_contact_details(self):
        """Invalid contact details must not create a reservation."""

        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "",
                "email": "invalid-email",
                "phone": "",
                "product_ids": [str(self.product_one.pk)],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors below.")
        self.assertContains(response, "Enter a valid email address.")
        self.assertEqual(Order.objects.count(), 0)

    def test_successful_reservation_redirects_to_confirmation(self):
        """A successful reservation redirects to its confirmation page."""

        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "john@example.com",
                "phone": "07123456789",
                "product_ids": [str(self.product_one.pk)],
            },
        )

        order = Order.objects.get()

        self.assertRedirects(
            response,
            reverse("reservation_confirmation", args=[order.pk]),
        )

    def test_invalid_contact_details_display_form_errors(self):
        """Invalid contact details should display errors
        without losing input."""

        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "John Smith",
                "email": "invalid-email",
                "phone": "07123456789",
                "product_ids": [str(self.product_one.pk)],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.")
        self.assertContains(response, "John Smith")
        self.assertContains(response, "07123456789")
        self.assertEqual(Order.objects.count(), 0)

    def test_reservation_succeeds_after_correcting_invalid_email(self):
        """Customers can correct invalid details and complete a reservation."""

        data = {
            "customer_name": "John Smith",
            "email": "invalid-email",
            "phone": "07123456789",
            "product_ids": [str(self.product_one.pk)],
        }

        # First submission contains an invalid email.
        response = self.client.post(
            reverse("reservation_create"),
            data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)

        # Customer corrects the email and submits again.
        data["email"] = "john@example.com"

        response = self.client.post(
            reverse("reservation_create"),
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get()

        self.assertEqual(order.items.count(), 1)
        self.assertEqual(
            order.items.first().product,
            self.product_one,
        )


class ReservationConfirmationTests(TestCase):
    """Tests for the reservation confirmation page."""

    def setUp(self):
        self.category = Category.objects.create(name="Kohaku")

        self.order = Order.objects.create(
            customer_name="John Smith",
            email="john@example.com",
            phone="07123456789",
            total_price=Decimal("600.00"),
        )

    def test_confirmation_page_returns_200(self):
        """An existing reservation should have a confirmation page."""
        response = self.client.get(
            reverse(
                "reservation_confirmation",
                args=[self.order.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_confirmation_page_displays_order_details(self):
        """The confirmation page should display reservation information."""
        response = self.client.get(
            reverse(
                "reservation_confirmation",
                args=[self.order.pk],
            )
        )

        self.assertContains(response, f"Reservation #{self.order.pk}")
        self.assertContains(response, "600.00")

    def test_confirmation_page_returns_404_for_missing_order(self):
        """A nonexistent reservation should return HTTP 404."""
        response = self.client.get(
            reverse(
                "reservation_confirmation",
                args=[999999],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_confirmation_displays_primary_image(self):
        """Display the reserved product's primary image."""

        product = Product.objects.create(
            name="Japanese Kohaku",
            category=self.category,
            price=250.00,
            size=35,
            age=2,
        )

        OrderItem.objects.create(
            order=self.order,
            product=product,
            price=product.price,
        )

        primary_image = ProductImage.objects.create(
            product=product,
            image=CloudinaryImage("products/test_primary"),
            is_primary=True,
        )

        response = self.client.get(
            reverse("reservation_confirmation", args=[self.order.pk])
        )

        self.assertContains(response, primary_image.image.url)

    def test_confirmation_displays_fallback_image(self):
        """Display a placeholder when the product has no primary image."""

        product = Product.objects.create(
            name="Japanese Kohaku",
            category=self.category,
            price=250.00,
            size=35,
            age=2,
        )

        OrderItem.objects.create(
            order=self.order,
            product=product,
            price=product.price,
        )

        response = self.client.get(
            reverse("reservation_confirmation", args=[self.order.pk])
        )

        self.assertContains(
            response,
            staticfiles_storage.url("images/default.png"),
        )


class OrderAdminTests(TestCase):
    """Test reservation management in Django Admin."""

    def setUp(self):
        self.category = Category.objects.create(name="Kohaku")
        self.product = Product.objects.create(
            name="Japanese Kohaku",
            category=self.category,
            price=Decimal("250.00"),
            size=30,
            age=2,
            status=Product.ProductStatus.RESERVED,
        )

        self.order = Order.objects.create(
            customer_name="Test Customer",
            email="test@example.com",
            phone="07123456789",
            total_price=Decimal("250.00"),
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
        )

    def test_cancelling_order_releases_product(self):
        """Cancelling a reservation makes its koi available again."""
        order_admin = OrderAdmin(Order, AdminSite())

        self.order.status = Order.OrderStatus.CANCELLED
        order_admin.save_model(
            request=None,
            obj=self.order,
            form=None,
            change=True,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.status,
            Product.ProductStatus.AVAILABLE,
        )

    def test_confirming_order_keeps_product_reserved(self):
        """Confirming an order must not release its reserved koi."""
        order_admin = OrderAdmin(Order, AdminSite())

        self.order.status = Order.OrderStatus.CONFIRMED

        order_admin.save_model(
            request=None,
            obj=self.order,
            form=None,
            change=True,
        )

        self.order.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.OrderStatus.CONFIRMED,
        )

        self.assertEqual(
            self.product.status,
            Product.ProductStatus.RESERVED,
        )

    def test_anonymous_user_cannot_access_orders_admin(self):
        """Anonymous users cannot access reservation management."""

        response = self.client.get(
            reverse("admin:orders_order_changelist")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)


class CartPageTests(TestCase):
    """Tests for the shopping cart page."""

    def test_cart_page_renders(self):
        """The cart page should render successfully."""
        response = self.client.get("/cart/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/cart.html")

    def test_cart_page_contains_reservation_form(self):
        """The cart page should contain a reservation form."""
        response = self.client.get("/cart/")

        self.assertContains(response, 'id="reservation-form"')
        self.assertContains(response, 'method="post"')
        self.assertContains(
            response,
            f'action="{reverse("reservation_create")}"'
        )
        self.assertContains(response, 'name="customer_name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="phone"')
        self.assertContains(response, 'type="submit"')

    def test_cart_displays_breadcrumbs(self):
        """Display Home and Cart breadcrumbs on the cart page."""
        response = self.client.get(reverse("cart"))

        self.assertContains(
            response,
            '<nav class="breadcrumbs" aria-label="Breadcrumb">'
        )
        self.assertContains(
            response,
            '<span aria-current="page">Cart</span>'
        )


class CartProductsTests(TestCase):
    """Tests for retrieving product details for the shopping cart."""

    def test_returns_requested_products(self):
        """The endpoint should return details of requested products."""
        category = Category.objects.create(name="Kohaku")

        product = Product.objects.create(
            name="Japanese Kohaku",
            category=category,
            price=Decimal("150.00"),
            size=30,
            age=2,
        )

        response = self.client.get(
            "/cart/products/",
            {"ids": [product.pk]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["products"][0]["name"],
            "Japanese Kohaku",
        )

    def test_returns_primary_product_image_url(self):
        """Return the primary Cloudinary image URL for a cart product."""
        category = Category.objects.create(name="Kohaku")

        product = Product.objects.create(
            name="Japanese Kohaku",
            category=category,
            price=Decimal("150.00"),
            size=30,
            age=2,
        )

        ProductImage.objects.create(
            product=product,
            image="koi4sale/products/test-kohaku",
            is_primary=True,
        )

        # Reload the image from the database to obtain the
        # Cloudinary field value instead of the assigned string.
        image = ProductImage.objects.get(product=product)

        response = self.client.get(
            reverse("cart_products"),
            {"ids": [product.pk]},
        )

        self.assertEqual(response.status_code, 200)

        product_data = response.json()["products"][0]

        self.assertEqual(
            product_data["image_url"],
            image.image.url,
        )

    def test_returns_fallback_image_when_no_primary_exists(self):
        """Return the default image when a koi has no primary photo."""
        category = Category.objects.create(name="Kohaku")

        product = Product.objects.create(
            name="Japanese Kohaku",
            category=category,
            price=Decimal("150.00"),
            size=30,
            age=2,
        )

        response = self.client.get(
            reverse("cart_products"),
            {"ids": [product.pk]},
        )

        self.assertEqual(response.status_code, 200)

        product_data = response.json()["products"][0]

        # Use Django's static files storage to support
        # WhiteNoise's hashed filenames in production.
        self.assertEqual(
            product_data["image_url"],
            staticfiles_storage.url("images/default.png"),
        )
