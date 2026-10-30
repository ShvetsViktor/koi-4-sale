from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView, DeleteView

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
            messages.success(
                request,
                "Your account has been created successfully.",
            )
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

    def form_valid(self, form):
        """Confirm successful profile updates."""
        messages.success(
            self.request,
            "Your profile has been updated successfully.",
        )
        return super().form_valid(form)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """Allow authenticated users to delete their own account."""

    template_name = "accounts/account_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        """Return the currently authenticated user."""
        return self.request.user

    def form_valid(self, form):
        """Delete the account and terminate the user session."""
        response = super().form_valid(form)
        logout(self.request)
        return response
