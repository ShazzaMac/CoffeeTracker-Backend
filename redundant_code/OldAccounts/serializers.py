from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)  # Get email from User model

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'phone', 'about', 'profile_photo']
