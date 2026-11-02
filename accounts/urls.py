from django.urls import path

from .views import (
    AccountDeleteView,
    CustomLogoutView,
    ProfileUpdateView,
    ProfileView,
    SignUpView,
)


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path(
        "profile/delete/",
        AccountDeleteView.as_view(),
        name="account_delete",
    ),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
