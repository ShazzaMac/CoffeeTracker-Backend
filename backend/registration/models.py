# Django imports - this is the default Django User model and the AbstractUser class that we will inherit from.
# registration/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Add related_name to resolve clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set',  # Specify a custom reverse relation
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permissions',  # Specify a custom reverse relation
        blank=True
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # Fields you want to require at creation
