from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView

from .forms import ProfileUpdateForm, SignUpForm


class SignUpView(View):
    """Handle customer account registration."""

    def get(self, request):
        """Display the registration form."""
        return render(
            request,
            "accounts/signup.html",
            {"form": SignUpForm()},
        )

    def post(self, request):
        """Validate registration details and create a user."""
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

        return render(
            request,
            "accounts/signup.html",
            {"form": form},
        )


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display the authenticated user's profile."""

    template_name = "accounts/profile.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Allow authenticated users to edit their own profile."""

    form_class = ProfileUpdateForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        """Return the currently authenticated user."""
        return self.request.user
