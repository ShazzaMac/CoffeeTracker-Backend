from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from registration.serializers import UserLoginSerializer, UserRegistrationSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core import mail
from django.contrib.auth.models import User
from mycoffeeapp.models import CoffeeShop


User = get_user_model()


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

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_registration_missing_fields(self):
        response = self.client.post(self.register_url, {"username": "testuser"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

        user = User.objects.get(username="testuser")
        self.assertTrue(Token.objects.filter(user=user).exists())


class UserRegistrationSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
        }

    def setUp(self):
        self.user_data = self.__class__.user_data

    def test_user_registration_serializer_valid(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_user_registration_serializer_saves_user(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_user_registration_serializer_missing_fields(self):
        incomplete_data = {"username": "testuser"}
        serializer = UserRegistrationSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())


class UserLoginSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_user_login_serializer_valid(self):
        data = {"username": "testuser", "password": "testpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["username"], data["username"])

    def test_user_login_serializer_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"], ["Invalid credentials"])


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
        cls.user_login_data = {"username": "testuser", "password": "testpassword"}

    def test_user_registration_view(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_login_view(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

        user = User.objects.get(username="testuser")
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_user_login_serializer_invalid_credentials(self):
        self.client.post(self.register_url, self.user_data, format="json")
        invalid_login = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, invalid_login, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials")

class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="forgotuser", email="forgot@example.com", password="testpass123")
        self.url = reverse("forgot-password")  # Make sure this URL is set up correctly

    def test_send_new_password_success(self):
        response = self.client.post(self.url, {"email": "forgot@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Your new temporary password", mail.outbox[0].body)

    def test_forgot_password_user_not_found(self):
        response = self.client.post(self.url, {"email": "nonexistent@example.com"})
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.data)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class ResetPasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="resetuser", email="reset@example.com", password="oldpassword")
        self.token = default_token_generator.make_token(self.user)
        self.uid = self.user.pk
        self.url = reverse("reset-password", kwargs={"uid": self.uid, "token": self.token})

    def test_password_reset_successful(self):
        response = self.client.post(self.url, {"password": "newpass123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Password reset successfully.")

    def test_password_reset_invalid_token(self):
        invalid_url = reverse("reset-password", kwargs={"uid": self.uid, "token": "invalidtoken"})
        response = self.client.post(invalid_url, {"password": "newpass123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

from rest_framework_simplejwt.tokens import RefreshToken

class ProtectedEndpointTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="protecteduser", password="testpass")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client = APIClient()
        self.url = reverse("protected-endpoint")

    def test_access_protected_with_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "You have access!")

    def test_access_protected_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

class DashboardViewTest(TestCase):
    def test_dashboard_access(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

def test_password_reset_missing_password(self):
    response = self.client.post(self.url, {})
    self.assertEqual(response.status_code, 400)
    self.assertIn("error", response.json())
