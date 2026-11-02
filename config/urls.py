"""Define the main URL routes for Koi4Sale."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from products.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("products/", include("products.urls")),
    path(
        "delivery/",
        TemplateView.as_view(template_name="delivery.html"),
        name="delivery",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="contact.html"),
        name="contact",
    ),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("orders.urls")),
]
