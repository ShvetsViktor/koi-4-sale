from decimal import Decimal

from django.test import TestCase

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