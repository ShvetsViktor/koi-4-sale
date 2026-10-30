from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from orders.models import Order


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

    def test_signup_form_uses_crispy_bootstrap5(self):
        """Render the registration form with Bootstrap 5 styling."""
        response = self.client.get(reverse("signup"))

        self.assertContains(response, 'class="textinput form-control"')
        self.assertContains(response, 'class="emailinput form-control"')
        self.assertContains(response, 'class="passwordinput form-control"')

    def test_successful_registration_displays_success_message(self):
        """Display a success message after successful registration."""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "SecurePassword123!",
                "password2": "SecurePassword123!",
            },
            follow=True,
        )

        messages = list(response.context["messages"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Your account has been created successfully.",
        )

    def test_registration_success_message_is_displayed_in_html(self):
        """Display the registration success message on the login page."""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "SecurePassword123!",
                "password2": "SecurePassword123!",
            },
            follow=True,
        )

        self.assertContains(
            response,
            "Your account has been created successfully.",
        )
        self.assertContains(response, 'role="status"')


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

    def test_login_form_uses_crispy_bootstrap5(self):
        """Render the login form with Bootstrap 5 styling."""
        response = self.client.get(reverse("login"))

        self.assertContains(response, 'class="textinput form-control"')
        self.assertContains(response, 'class="passwordinput form-control"')


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

    def test_profile_does_not_display_another_users_details(self):
        """Ensure users cannot view another user's profile details."""
        User.objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="SecurePassword123!",
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))

        self.assertContains(response, "testuser")
        self.assertNotContains(response, "anotheruser")
        self.assertNotContains(response, "another@example.com")

    def test_profile_displays_edit_link(self):
        """Display the profile editing link for authenticated users."""
        self.client.force_login(self.user)

        response = self.client.get(reverse("profile"))

        self.assertContains(
            response,
            f'href="{reverse("profile_edit")}"',
        )

    def test_profile_displays_delete_account_link(self):
        """Display the account deletion link for authenticated users."""
        self.client.force_login(self.user)

        response = self.client.get(reverse("profile"))

        self.assertContains(
            response,
            f'href="{reverse("account_delete")}"',
        )


class UserProfileUpdateTests(TestCase):
    """Test customer profile editing."""

    def setUp(self):
        """Create a user for profile update tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="old@example.com",
            password="SecurePassword123!",
        )

    def test_authenticated_user_can_update_profile(self):
        """Allow authenticated users to update their account details."""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile_edit"),
            {
                "first_name": "Viktor",
                "last_name": "Shvets",
                "email": "new@example.com",
            },
        )

        # Reload the user from the database to verify that changes were saved.
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.first_name, "Viktor")
        self.assertEqual(self.user.last_name, "Shvets")
        self.assertEqual(self.user.email, "new@example.com")

    def test_invalid_email_does_not_update_profile(self):
        """Reject invalid email and preserve existing user details."""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile_edit"),
            {
                "first_name": "Viktor",
                "last_name": "Shvets",
                "email": "invalid-email",
            },
        )

        # Reload the user from the database to verify that changes were saved.
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "email",
            "Enter a valid email address.",
        )
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")
        self.assertEqual(self.user.email, "old@example.com")

    def test_anonymous_user_cannot_update_profile(self):
        """Redirect anonymous users without modifying account details."""
        response = self.client.post(
            reverse("profile_edit"),
            {
                "first_name": "Viktor",
                "last_name": "Shvets",
                "email": "new@example.com",
            },
        )

        self.user.refresh_from_db()

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile_edit')}",
            fetch_redirect_response=False,
        )
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")
        self.assertEqual(self.user.email, "old@example.com")

    def test_user_cannot_update_another_users_profile(self):
        """Ensure profile updates affect only the authenticated user."""
        another_user = User.objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="SecurePassword123!",
        )

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile_edit"),
            {
                "first_name": "Viktor",
                "last_name": "Shvets",
                "email": "new@example.com",
            },
        )

        self.user.refresh_from_db()
        another_user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.first_name, "Viktor")
        self.assertEqual(self.user.email, "new@example.com")

        self.assertEqual(another_user.first_name, "")
        self.assertEqual(another_user.last_name, "")
        self.assertEqual(another_user.email, "another@example.com")

    def test_successful_profile_update_displays_success_message(self):
        """Display a success message after updating profile details."""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile_edit"),
            {
                "first_name": "Viktor",
                "last_name": "Shvets",
                "email": "new@example.com",
            },
            follow=True,
        )

        self.assertContains(
            response,
            "Your profile has been updated successfully.",
        )
        self.assertContains(response, 'role="status"')


class UserAccountDeletionTests(TestCase):
    """Test customer account deletion."""

    def setUp(self):
        """Create a user for account deletion tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="SecurePassword123!",
        )

    def test_authenticated_user_can_delete_account(self):
        """Delete the authenticated user's account after POST confirmation."""
        self.client.force_login(self.user)

        response = self.client.post(reverse("account_delete"))

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(
            User.objects.filter(pk=self.user.pk).exists()
        )
        # Verify that the user is logged out after account deletion.
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_get_request_does_not_delete_account(self):
        """Display confirmation without deleting the user account."""
        self.client.force_login(self.user)

        response = self.client.get(reverse("account_delete"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/account_confirm_delete.html",
        )
        self.assertTrue(
            User.objects.filter(pk=self.user.pk).exists()
        )
        self.assertIn("_auth_user_id", self.client.session)

    def test_anonymous_user_cannot_delete_account(self):
        """Prevent anonymous users from deleting accounts."""
        response = self.client.post(reverse("account_delete"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('account_delete')}",
            fetch_redirect_response=False,
        )

        self.assertTrue(
            User.objects.filter(pk=self.user.pk).exists()
        )

    def test_account_deletion_preserves_existing_reservations(self):
        """Preserve reservation records after account deletion."""
        order = Order.objects.create(
            customer_name="Test User",
            email="test@example.com",
            phone="07712345678",
            total_price="100.00",
        )

        self.client.force_login(self.user)

        response = self.client.post(reverse("account_delete"))

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(
            User.objects.filter(pk=self.user.pk).exists()
        )
        self.assertTrue(
            Order.objects.filter(pk=order.pk).exists()
        )

    def test_successful_account_deletion_displays_success_message(self):
        """Display a success message after deleting an account."""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("account_delete"),
            follow=True,
        )

        self.assertContains(
            response,
            "Your account has been deleted successfully.",
        )
        self.assertContains(response, 'role="status"')
        self.assertFalse(
            User.objects.filter(pk=self.user.pk).exists()
        )
