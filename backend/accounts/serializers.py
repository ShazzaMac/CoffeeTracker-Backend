# -------------------------------------------------------------------
# This file contains serializers for the UserProfile model.
# It includes a serializer for the user profile and a serializer for changing the password.
# ----------------------------------------------------------------------
from django.contrib.auth.models import User
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]  # Add more fields if needed over time


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
