from django.views.generic import ListView
from .models import Product

# Create your views here.


class ProductList(ListView):
    model = Product
    queryset = Product.objects.filter(status=Product.ProductStatus.AVAILABLE)
    template_name = "products/product_list.html"
    context_object_name = "products"
