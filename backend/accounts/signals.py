# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # If the user is newly created, create a profile for it.
        UserProfile.objects.create(user=instance, email=instance.email)
    else:
        # For existing users, attempt to update the profile.
        try:
            instance.profile.save()
        except UserProfile.DoesNotExist:
            # If the profile doesn't exist, create one.
            UserProfile.objects.create(user=instance, email=instance.email)
