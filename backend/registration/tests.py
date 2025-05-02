# ----------------------------------------------------------------
# This file contains test cases for user registration, login,
# password reset, and protected endpoints using Django and DRF.
# references: https://docs.djangoproject.com/en/5.2/topics/testing/overview/
# references:https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing
# ----------------------------------------------------------------

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from registration.serializers import UserLoginSerializer, UserRegistrationSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core import mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator



User = get_user_model()


# ------------------------------
# User Registration & Login Tests
# ------------------------------
class UserRegistrationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.register_url = reverse("register")
        cls.login_url = reverse("login")
        cls.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
        }
        cls.user_login_data = {"username": "testuser", "password": "testpassword"}

    # This is a test for successful user registration
    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    # tests that an error is returned if there are missing fields
    def test_user_registration_missing_fields(self):
        response = self.client.post(
            self.register_url, {"username": "testuser"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user login with correct credentials
    def test_user_login(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])


# ------------------------------
# Serializer Tests
# ------------------------------
class UserRegistrationSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
        }

    # tests that the serializer is valid with correct data
    def test_user_registration_serializer_valid(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    # tests that the serializer saves the correct data
    def test_user_registration_serializer_saves_user(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.user_data["username"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    # tests that the serializer is invalid with missing fields
    def test_user_registration_serializer_missing_fields(self):
        incomplete_data = {"username": "testuser"}
        serializer = UserRegistrationSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())


class UserLoginSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    # tests that the login serializer is validated with correct credentials
    def test_user_login_serializer_valid(self):
        data = {"username": "testuser", "password": "testpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["username"], data["username"])

    # tests that the login serializer fails with incorrect password
    def test_user_login_serializer_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["non_field_errors"], ["Invalid credentials"])


# ------------------------------
# View Tests for Registration & Login
# ------------------------------
class UserRegistrationViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.register_url = reverse("register")
        cls.login_url = reverse("login")
        cls.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
        }

    # tests that the registration view returns a 201 status code to show that the endpoint works
    def test_user_registration_view(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # tests that login view returns JWT tokens when successful
    def test_user_login_view(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # tests login view fails on invalid credentials
    def test_user_login_serializer_invalid_credentials(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid credentials")


# ------------------------------
# Forgot Password View Test
# ------------------------------
class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="forgotuser", email="forgot@example.com", password="testpass123"
        )
        self.url = reverse("forgot-password")

    # tests email is sent on valid forgot password request
    def test_send_new_password_success(self):
        response = self.client.post(self.url, {"email": "forgot@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Your new temporary password", mail.outbox[0].body)

    # tests error returned if email address is not found
    def test_forgot_password_user_not_found(self):
        response = self.client.post(self.url, {"email": "nonexistent@example.com"})
        self.assertEqual(response.status_code, 404)


# ------------------------------
# Reset Password View Test
# ------------------------------
class ResetPasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="resetuser", email="reset@example.com", password="oldpassword"
        )
        self.token = default_token_generator.make_token(self.user)
        self.uid = self.user.pk
        self.url = reverse(
            "reset-password", kwargs={"uid": self.uid, "token": self.token}
        )

    # Tests that the password reset view returns a valid token
    def test_password_reset_successful(self):
        response = self.client.post(self.url, {"password": "newpass123"})
        self.assertEqual(response.status_code, 200)

    # tests that password reset fails with invalid token
    def test_password_reset_invalid_token(self):
        url = reverse(
            "reset-password", kwargs={"uid": self.uid, "token": "invalidtoken"}
        )
        response = self.client.post(url, {"password": "newpass123"})
        self.assertEqual(response.status_code, 400)
