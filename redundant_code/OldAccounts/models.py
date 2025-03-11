from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Changed 'username' to 'user'
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    about = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    class Meta:
        app_label = 'accounts'  
    
    def __str__(self):
        return self.user.username  # This now correctly references the User model
