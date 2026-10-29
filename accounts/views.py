from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View

from .forms import SignUpForm


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