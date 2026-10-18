from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.db.models import Prefetch
from django.contrib.staticfiles.storage import staticfiles_storage

from products.models import Product, ProductImage

from .forms import ReservationForm
from .models import Order, OrderItem


class ReservationCreate(View):
    """Handle customer reservation requests."""

    def post(self, request):
        form = ReservationForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "orders/cart.html",
                {"form": form},
            )

        product_ids = request.POST.getlist("product_ids")

        if not product_ids:
            return HttpResponseBadRequest("No koi selected.")

        try:
            product_ids = [int(pk) for pk in product_ids]
        except ValueError:
            return HttpResponseBadRequest("Invalid product IDs.")

        if len(product_ids) != len(set(product_ids)):
            return HttpResponseBadRequest("Duplicate product IDs.")

        with transaction.atomic():
            products = list(
                Product.objects.select_for_update()
                .filter(pk__in=product_ids)
                .order_by("pk")
            )

            if len(products) != len(product_ids):
                return HttpResponseBadRequest(
                    "One or more selected koi do not exist."
                )

            if any(
                product.status != Product.ProductStatus.AVAILABLE
                for product in products
            ):
                return HttpResponseBadRequest(
                    "One or more selected koi are unavailable."
                )

            order = form.save(commit=False)
            order.total_price = sum(
                product.price for product in products
            )
            order.save()

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=product,
                    price=product.price,
                )
                for product in products
            ])

            Product.objects.filter(
                pk__in=product_ids
            ).update(
                status=Product.ProductStatus.RESERVED
            )

        return redirect("reservation_confirmation", pk=order.pk)


class ReservationConfirmation(DetailView):
    """Display confirmation details for a submitted reservation."""

    model = Order
    template_name = "orders/reservation_confirmation.html"
    context_object_name = "order"


class CartView(TemplateView):
    """Display the shopping cart page."""

    template_name = "orders/cart.html"


class CartProductsView(View):
    """Return product details for the shopping cart."""

    def get(self, request):
        """Retrieve products matching the requested IDs."""
        product_ids = request.GET.getlist("ids")

        # Fetch primary images separately to avoid additional database
        # queries for each product when building the JSON response.
        products = Product.objects.filter(
            pk__in=product_ids
        ).prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_primary=True),
                to_attr="primary_images",
            )
        )

        # Use the primary Cloudinary image when available.
        # Otherwise, return the static placeholder image.
        product_data = [
            {
                "id": product.pk,
                "name": product.name,
                "price": str(product.price),
                "status": product.status,
                "image_url": (
                    product.primary_images[0].image.url
                    if product.primary_images
                    else staticfiles_storage.url("images/default.png")
                ),
            }
            for product in products
        ]

        return JsonResponse({"products": product_data})
