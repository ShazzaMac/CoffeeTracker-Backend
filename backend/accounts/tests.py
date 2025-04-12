# Description: This file contains the tests for the accounts app.
# The tests all pass successfully. updated --- as of 25/03/25
# Additional coverage tested -30/03/25
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from accounts.serializers import UserProfileSerializer
from accounts.models import UserProfile
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
        # Email is optional so should still pass 
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


# Test signal
class UserProfileSignalTest(TestCase):
    def test_user_profile_created_on_user_creation(self):
        user = User.objects.create_user(
            username='signaltest',
            email='signal@example.com',
            password='testpass123'
        )
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

class UserProfileSignalNoDuplicateTest(TestCase):
    def test_user_profile_not_created_again_on_update(self):
        user = User.objects.create_user(
            username='nodupetest',
            email='dup@example.com',
            password='password'
        )
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

        # Update user – should NOT create another profile
        user.first_name = "Changed"
        user.save()
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

class PasswordChangeViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='changepw',
            email='changepw@example.com',
            password='oldpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.url = "/api/accounts/change-password/"

    def test_password_change_successful(self):
        data = {
            'current_password': 'oldpassword',
            'new_password': 'newsecurepassword123'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Password changed successfully", response.data["detail"])

        # Confirm new password works
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword123"))

    def test_password_change_wrong_current_password(self):
        data = {
            'current_password': 'wrongpassword',
            'new_password': 'whatever123'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Current password is incorrect", response.data["detail"])

    def test_password_change_missing_fields(self):
        response = self.client.post(self.url, data=json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("current_password", response.data)
        self.assertIn("new_password", response.data)

    def test_password_change_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            'current_password': 'oldpassword',
            'new_password': 'newpassword123'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)

