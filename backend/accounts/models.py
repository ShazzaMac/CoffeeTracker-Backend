# backend/accounts/models.py
from django.db import models
from django.contrib.auth.models import User # Import the User model from Django

class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    about = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    class Meta:
        app_label = 'accounts'  # Explicitly specify the app label if it's not in the default location
    
    def __str__(self):
        return self.user.username

