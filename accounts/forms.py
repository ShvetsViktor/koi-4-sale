from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class SignUpForm(UserCreationForm):
    """Handle customer registration details."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileUpdateForm(forms.ModelForm):
    """Allow users to update their account details."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
