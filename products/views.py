from django.db.models import Prefetch
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Product, ProductImage


class ProductList(ListView):
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.filter(
            status=Product.ProductStatus.AVAILABLE
        ).prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_primary=True),
                to_attr="primary_images",
            )
        )

        category_id = self.request.GET.get("category")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
