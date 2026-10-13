from django.db import models

# Create your models here.

STATUS = [("available", "Available"), ("not_available", "Not_Available"),]


class Product(models.Model):
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=50)
    size = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    details = models.TextField()
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS,
                              default="available")
