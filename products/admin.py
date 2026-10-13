from django.contrib import admin
from .models import Product, Category


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
