from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView

from products.models import Product

from .forms import ReservationForm
from .models import Order, OrderItem


class ReservationCreate(View):
    """Handle customer reservation requests."""

    def post(self, request):
        form = ReservationForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest("Invalid contact details.")

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
