# -----------------------------------------------------------
# This file contains the UserProfile model, which extends the default Django User model.
# It includes an email field and a one-to-one relationship with the User model.
# -----------------------------------------------------------
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(max_length=255, blank=True)

    class Meta:
        app_label = "accounts"

    def __str__(self):
        return self.user.username
