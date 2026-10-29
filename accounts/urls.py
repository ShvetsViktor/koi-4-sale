from django.urls import path

from .views import (
    SignUpView,
    ProfileView,
    ProfileUpdateView,
    AccountDeleteView,
)


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/delete/", AccountDeleteView.as_view(),
         name="account_delete"),
]
