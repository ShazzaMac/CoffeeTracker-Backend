# This set up is for creating a custom user registration form rather than using the default Django User model.
# This is useful if you need additional fields or customization for your user registration process.
# This inherits from the default Django User model in models.py and adds any additional fields needed for registration.

from django import forms

from .models import CustomUser  # Import your custom user model


class CustomUserCreationForm(forms.ModelForm):
    # Add any additional fields to the registration form if needed
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]  # Include custom fields if necessary
