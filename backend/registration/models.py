# Django imports - this is the default Django User model and the AbstractUser class that we will inherit from.
# registration/models.py
# models are used to define the structure of the database so each model is a table in the database
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

class CoffeeShop(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    average_price = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.FloatField()
    most_popular_coffee = models.CharField(max_length=255)

    def __str__(self):
        return self.name