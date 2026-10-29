from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.db.models import Prefetch
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import messages

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
                messages.error(
                    request,
                    "One or more selected koi are no longer available. "
                    "Please review your cart."
                )
                return redirect("cart")

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

        return redirect(
            "reservation_confirmation",
            access_token=order.access_token,
        )


class ReservationConfirmation(DetailView):
    """Display confirmation details for a submitted reservation."""

    model = Order
    template_name = "orders/reservation_confirmation.html"
    context_object_name = "order"
    slug_field = "access_token"
    slug_url_kwarg = "access_token"


class CartView(TemplateView):
    """Display the shopping cart page."""

    template_name = "orders/cart.html"

    def get_context_data(self, **kwargs):
        """Provide the reservation form to the template."""
        context = super().get_context_data(**kwargs)
        context["form"] = ReservationForm()
        return context


class CartProductsView(View):
    """Return product details for the shopping cart."""

    def get(self, request):
        """Retrieve products matching the requested IDs."""
        product_ids = request.GET.getlist("ids")

        try:
            product_ids = [int(pk) for pk in product_ids]
        except ValueError:
            return HttpResponseBadRequest("Invalid product IDs.")

        products = list(
            Product.objects.filter(
                pk__in=product_ids
            ).prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_primary=True),
                    to_attr="primary_images",
                )
            )
        )

        if len(products) != len(set(product_ids)):
            return HttpResponseBadRequest(
                "One or more products do not exist."
            )

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
