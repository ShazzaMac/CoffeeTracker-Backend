# This file is for unit tests for the registration app.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from registration_api.serializers import (  # Import serializers
    UserLoginSerializer, UserRegistrationSerializer)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()  # Use get_user_model for custom user models


# class to test the user registration
class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user = {
            "email": "testuser@example.com",  # Complete the email field
            "username": "testuser",
            "password": "testpassword",
        }
        self.user_login = {"username": "testuser", "password": "testpassword"}

    def test_user_registration(self):
        # Test the registration API endpoint
        response = self.client.post(self.register_url, self.user, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_login(self):
        # Test the login API endpoint
        self.client.post(self.register_url, self.user, format="json")
        response = self.client.post(self.login_url, self.user_login, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)  # Check if token exists


# class to test the user registration serializer
class UserRegistrationSerializerTestCase(TestCase):
    def setUp(self):
        self.user = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
        }

    def test_user_registration_serializer(self):
        # Test the serializer for user registration
        serializer = UserRegistrationSerializer(data=self.user)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.user["username"])
        self.assertEqual(user.email, self.user["email"])
        self.assertTrue(user.check_password(self.user["password"]))


# create a class to test the user login serializer
class UserLoginSerializerTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_user_login_serializer(self):
        # Test the login serializer
        data = {"username": "testuser", "password": "testpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["username"], data["username"])


# class to test the user registration view
class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
        }
        self.user_login = {"username": "testuser", "password": "testpassword"}

    def test_user_registration_view(self):
        # Test the registration view
        response = self.client.post(self.register_url, self.user, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_login_view(self):
        # Test the login view
        self.client.post(self.register_url, self.user, format="json")
        response = self.client.post(self.login_url, self.user_login, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
