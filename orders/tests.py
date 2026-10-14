from decimal import Decimal

from django.test import TestCase
from .forms import ReservationForm

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
