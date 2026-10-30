from django.db.models.signals import pre_delete
from django.dispatch import receiver

from products.models import Product
from .models import Order


@receiver(pre_delete, sender=Order)
def release_products_on_order_delete(sender, instance, **kwargs):
    """Release reserved koi when their reservation is deleted."""
    product_ids = instance.items.values_list("product_id", flat=True)

    Product.objects.filter(
        pk__in=product_ids,
        status=Product.ProductStatus.RESERVED,
    ).update(status=Product.ProductStatus.AVAILABLE)
