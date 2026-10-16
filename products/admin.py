from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category, ProductImage


class ProductImageInline(admin.TabularInline):
    """Manage product images within the product admin page."""

    model = ProductImage
    extra = 1
    readonly_fields = ("image_preview",)
    fields = ("image", "image_preview", "is_primary")

    @admin.display(description="Preview")
    def image_preview(self, obj):
        """Display a thumbnail of the uploaded image."""
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" width="100" alt="Product image">',
                obj.image.url,
            )
        return "No image"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "size",
        "status",
        "created_on",
    )

    list_filter = ("category", "status")
    search_fields = ("name", "category__name")
    list_editable = ("status",)

    inlines = [ProductImageInline]