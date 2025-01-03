# registration/serializers.py (for DRF API)
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()  # This automatically uses the correct user model (CustomUser or User)
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)  # Create the user
        return user
