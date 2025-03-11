# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=255, blank=True)
    
    class Meta:
        app_label = 'accounts'
    
    def __str__(self):
        return self.user.username
