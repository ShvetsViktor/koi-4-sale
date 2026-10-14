from django.contrib import admin

from .models import Order, OrderItem
from products.models import Product


class OrderItemInline(admin.TabularInline):
    """Display reserved koi within an order."""

    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Manage customer reservations through Django Admin."""

    list_display = (
        "id",
        "customer_name",
        "email",
        "status",
        "total_price",
        "created_on",
    )

    list_filter = ("status", "created_on")

    search_fields = ("customer_name", "email")

    readonly_fields = (
        "customer_name",
        "email",
        "phone",
        "total_price",
        "created_on",
    )

    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        """Release reserved koi when an order is cancelled."""

        previous_status = None

        if change:
            previous_status = Order.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if (
            previous_status != Order.OrderStatus.CANCELLED
            and obj.status == Order.OrderStatus.CANCELLED
        ):
            products = Product.objects.filter(
                order_items__order=obj,
                status=Product.ProductStatus.RESERVED,
            )

            products.update(status=Product.ProductStatus.AVAILABLE)
