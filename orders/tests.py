from decimal import Decimal

from django.test import TestCase
from .forms import ReservationForm
from django.urls import reverse

from products.models import Category, Product
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
        """Invalid customer details must not create a reservation."""
        response = self.client.post(
            reverse("reservation_create"),
            {
                "customer_name": "",
                "email": "invalid-email",
                "phone": "",
                "product_ids": [str(self.product_one.pk)],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
