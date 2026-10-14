from django.db import models
from products.models import Product


class Order(models.Model):
    """A customer reservation request containing one or more koi."""

    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"


class OrderItem(models.Model):
    """An individual koi included in a reservation request."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_product_per_order",
            ),
        ]

    def __str__(self):
        return f"{self.product.name} - Order #{self.order_id}"
