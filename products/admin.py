from django.contrib import admin
from .models import Product


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
