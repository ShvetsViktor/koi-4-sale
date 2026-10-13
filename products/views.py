from django.db.models import Prefetch
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Product, ProductImage


class ProductList(ListView):
    # Retrieve only available products and prefetch their primary images
    # to avoid additional database queries for each product.
    queryset = Product.objects.filter(
        status=Product.ProductStatus.AVAILABLE
    ).prefetch_related(
        Prefetch(
            "images",
            queryset=ProductImage.objects.filter(is_primary=True),
            to_attr="primary_images",
        )
    )

    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
