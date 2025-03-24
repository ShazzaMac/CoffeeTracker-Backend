from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from registration.serializers import UserLoginSerializer, UserRegistrationSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

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
