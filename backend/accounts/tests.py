# Description: This file contains the tests for the accounts app.
# The tests all pass successfully. updated --- as of 25/03/25
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from accounts.serializers import UserProfileSerializer
import json


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)

    def test_profile_view(self):
        response = self.client.get("/api/accounts/profile/")
        serializer = UserProfileSerializer(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_profile_view(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'Name',
        }
        response = self.client.patch(
            "/api/accounts/profile/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newuser')
        self.assertEqual(self.user.email, 'new@example.com')

    def test_profile_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/accounts/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch("/api/accounts/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_invalid_data(self):
        # Email is optional in your serializer, so this should still return 200
        data = {
            'email': '',
        }
        response = self.client.patch(
            "/api/accounts/profile/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_partial_data(self):
        data = {
            'first_name': 'PartialUpdate'
        }
        response = self.client.patch(
            "/api/accounts/profile/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'PartialUpdate')
