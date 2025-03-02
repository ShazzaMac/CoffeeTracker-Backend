from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
import json

class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.profile = UserProfile.objects.create(user=self.user, phone='1234567890')

    def test_profile_view(self):
        """
        Test the profile view to ensure it returns the correct user profile data
        """
        response = self.client.get(reverse('profile'))  # Adjust 'profile' with your actual URL name
        profile = UserProfile.objects.get(user=self.user)
        serializer = UserProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_view(self):
        """
        Test updating the user profile (username, email, password, phone)
        """
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'newpassword123',
            'phone': '0987654321',
        }
        response = self.client.post(reverse('update_profile'), data=json.dumps(data), content_type='application/json')  # Adjust 'update_profile' with your actual URL name
        self.assertEqual(response.data['message'], 'Profile updated successfully')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the changes in the database
        user = User.objects.get(username='newusername')
        self.assertEqual(user.email, 'newemail@example.com')
        self.assertTrue(user.check_password('newpassword123'))
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.phone, '0987654321')

    def test_profile_view_unauthenticated(self):
        """
        Test that an unauthenticated user cannot access the profile view
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('profile'))  # Adjust 'profile' with your actual URL name
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_view_unauthenticated(self):
        """
        Test that an unauthenticated user cannot update the profile
        """
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('update_profile'))  # Adjust 'update_profile' with your actual URL name
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
