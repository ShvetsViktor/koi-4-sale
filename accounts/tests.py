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


class UserLoginTests(TestCase):
    """Test customer login functionality."""

    def setUp(self):
        """Create a user for authentication tests."""
        self.user = User.objects.create_user(
            username="testuser",
            password="SecurePassword123!",
        )

    def test_login_page_returns_200(self):
        """Display the login page."""
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_valid_login_authenticates_user(self):
        """Authenticate a user with valid credentials."""
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "SecurePassword123!",
            },
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )
        self.assertRedirects(
            response,
            reverse("home"),
            fetch_redirect_response=False,
        )

    def test_invalid_login_is_rejected(self):
        """Reject login with an incorrect password."""
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "WrongPassword123!",
            },
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)


class UserLogoutTests(TestCase):
    """Test customer logout functionality."""

    def setUp(self):
        """Create and authenticate a user."""
        self.user = User.objects.create_user(
            username="testuser",
            password="SecurePassword123!",
        )
        self.client.force_login(self.user)

    def test_logout_redirects_to_home(self):
        """Redirect users to the homepage after logout."""
        response = self.client.post(reverse("logout"))

        self.assertRedirects(
            response,
            reverse("home"),
            fetch_redirect_response=False,
        )

    def test_logout_ends_authenticated_session(self):
        """End the authenticated session after logout."""
        self.client.post(reverse("logout"))

        response = self.client.get(reverse("home"))

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_get_request_does_not_logout_user(self):
        """Prevent logout through a GET request."""
        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse("home"))

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )


class AuthenticationNavigationTests(TestCase):
    """Test navigation links based on authentication status."""

    def test_guest_sees_login_and_signup(self):
        """Display login and signup links for guests."""
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'href="/accounts/login/"')
        self.assertContains(response, 'href="/accounts/signup/"')
        self.assertNotContains(response, 'action="/accounts/logout/"')

    def test_authenticated_user_sees_logout(self):
        """Display logout instead of login and signup."""
        user = User.objects.create_user(
            username="testuser",
            password="SecurePassword123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("home"))

        self.assertContains(response, 'action="/accounts/logout/"')
        self.assertNotContains(response, 'href="/accounts/login/"')
        self.assertNotContains(response, 'href="/accounts/signup/"')

    def test_authenticated_user_sees_profile_link(self):
        """Display the profile link for authenticated users."""
        user = User.objects.create_user(
            username="testuser",
            password="SecurePassword123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            f'href="{reverse("profile")}"',
        )

    def test_guest_does_not_see_profile_link(self):
        """Hide the profile link from anonymous users."""
        response = self.client.get(reverse("home"))

        self.assertNotContains(
            response,
            f'href="{reverse("profile")}"',
        )


class UserProfileTests(TestCase):
    """Test customer profile access."""

    def setUp(self):
        """Create a user for profile tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="SecurePassword123!",
        )

    def test_authenticated_user_can_view_profile(self):
        """Display the profile page for authenticated users."""
        self.client.force_login(self.user)

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertContains(response, "testuser")
        self.assertContains(response, "test@example.com")

    def test_anonymous_user_redirects_to_login(self):
        """Redirect anonymous users to the login page."""
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
            fetch_redirect_response=False,
        )

    def test_profile_displays_first_and_last_name(self):
        """Display the authenticated user's first and last name."""
        self.user.first_name = "Viktor"
        self.user.last_name = "Shvets"
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))

        self.assertContains(response, "Viktor")
        self.assertContains(response, "Shvets")
