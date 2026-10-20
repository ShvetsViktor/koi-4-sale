from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html

from .models import Product, Category, ProductImage


class ProductImageInlineFormSet(BaseInlineFormSet):
    """Ensure that each product has at most one primary image."""

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        primary_count = 0

        for form in self.forms:
            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            if form.cleaned_data.get("is_primary"):
                primary_count += 1

        if primary_count > 1:
            raise ValidationError(
                "Only one primary image is allowed per product."
            )


class ProductImageInline(admin.TabularInline):
    """Manage product images within the product admin page."""

    model = ProductImage
    formset = ProductImageInlineFormSet
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

    def save_formset(self, request, form, formset, change):
        """Save product images while preserving the primary selection."""

        instances = formset.save(commit=False)

        primary_image = next(
            (
                image_form.instance
                for image_form in formset.forms
                if image_form.cleaned_data
                and not image_form.cleaned_data.get("DELETE")
                and image_form.cleaned_data.get("is_primary")
            ),
            None,
        )

        if primary_image is not None:
            ProductImage.objects.filter(
                product=form.instance,
                is_primary=True,
            ).exclude(
                pk=primary_image.pk,
            ).update(is_primary=False)

        for obj in formset.deleted_objects:
            obj.delete()

        for instance in instances:
            instance.save()
