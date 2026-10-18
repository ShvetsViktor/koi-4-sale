from django.db import models
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    class ProductStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        SOLD = "sold", "Sold"
        UNAVAILABLE = "unavailable", "Unavailable"

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name="products",
                                 )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.AVAILABLE,
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = CloudinaryField("image", folder="koi4sale/products")
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_primary=True),
                name="unique_primary_image_per_product",
            )
        ]

    def __str__(self):
        return f"Image for {self.product.name}"
