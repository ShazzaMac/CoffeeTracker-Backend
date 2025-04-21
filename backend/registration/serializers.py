# ------------------------------------------------------------------
# serilaizers for the registration app
# ------------------------------------------------------------------

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import CustomUser

User = (
    get_user_model()
)  # This will get the custom user model first, otherwise it will default to the Django User model


# This serializer is used to validate and create a new user
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        error_messages={"min_length": "Password must be at least 8 characters long."},
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        # Ensure email is required
        extra_kwargs = {
            "email": {"required": True},
        }

    def create(self, validated_data):
        # Create a user and hash the password
        return User.objects.create_user(**validated_data)


# This serializer is used to validate user login credentials
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError(
                "Both username and password are required."
            )

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                {"non_field_errors": ["Invalid credentials"]}
            )

        return {
            "username": user.username,
            "password": password,
        }  # Ensures password is returned
