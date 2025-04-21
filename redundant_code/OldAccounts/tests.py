from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
import json
import os
from django.conf import settings
from django.contrib.auth.models import User


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.profile = UserProfile.objects.create(username=self.user, phone='1234567890', about='test about')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        profile = UserProfile.objects.get(username=self.user)
        serializer = UserProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_view(self):
        data = {
            'phone': '0987654321',  # Only update phone
            'about': 'updated about'
        }
        response = self.client.post(reverse('update_profile'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['message'], 'Profile updated successfully')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the changes in the database
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.phone, '0987654321')
        self.assertEqual(profile.about, 'updated about')

    def test_upload_photo_view(self):
        photo = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
        response = self.client.post(reverse('upload_photo'), {'photo': photo})
        self.assertEqual(response.data['profilePhoto'], '/media/test.jpg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the file has been saved in the media folder
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, 'test.jpg')))

    def test_upload_invalid_photo_view(self):
        invalid_photo = SimpleUploadedFile('test.txt', b'file_content', content_type='text/plain')
        response = self.client.post(reverse('upload_photo'), {'photo': invalid_photo})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('update_profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_photo_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('upload_photo'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
