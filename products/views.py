from django.db.models import Prefetch, Q
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product, ProductImage, Category


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

        query = self.request.GET.get("q", "").strip()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        # Extend the default template context with categories for filtering.
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetail(DetailView):
    """Display detailed information about an individual koi."""

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class HomeView(TemplateView):
    """Display the homepage."""

    template_name = "products/home.html"
