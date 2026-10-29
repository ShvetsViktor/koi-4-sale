from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserRegistrationTests(TestCase):
    """Test customer account registration."""

    def test_signup_page_returns_200(self):
        """Display the registration page."""
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_valid_registration_creates_user(self):
        """Create a user with valid registration details."""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "SecurePassword123!",
                "password2": "SecurePassword123!",
            },
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(
            User.objects.filter(username="testuser").exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_password_is_hashed(self):
        """Store the user's password securely."""
        self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "SecurePassword123!",
                "password2": "SecurePassword123!",
            },
        )

        user = User.objects.get(username="testuser")

        self.assertNotEqual(user.password, "SecurePassword123!")
        self.assertTrue(user.check_password("SecurePassword123!"))

    def test_duplicate_username_is_rejected(self):
        """Reject registration with an existing username."""
        User.objects.create_user(
            username="testuser",
            password="SecurePassword123!",
        )

        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "another@example.com",
                "password1": "SecurePassword123!",
                "password2": "SecurePassword123!",
            },
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_password_mismatch_is_rejected(self):
        """Reject registration when passwords do not match."""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "SecurePassword123!",
                "password2": "DifferentPassword123!",
            },
        )

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration_redirects_to_login(self):
        """Redirect newly registered users to the login page."""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "SecurePassword123!",
                "password2": "SecurePassword123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("login"),
            fetch_redirect_response=False,
        )