# ------------------------------------------------------------------
# Django imports - this is the default Django User model and the AbstractUser class that we will inherit from.
# registration/models.py
# models are used to define the structure of the database so each model is a table in the database
# ------------------------------------------------------------------
from django.contrib.auth.models import AbstractUser
from django.db import models


# This model is used to create a custom user model
# This is a custom user model that inherits from AbstractUser
# It includes additional fields such as email, first_name, and last_name
# The email field is set to be unique to ensure that no two users can have the same email address
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensures email is unique
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True,
    )

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
    ]  # Fields you want to require at creation


# the below model is used to store coffee shop information
# This is a placeholder for the coffee shop model
class CoffeeShop(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    average_price = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.FloatField()
    most_popular_coffee = models.CharField(max_length=255)

    def __str__(self):
        return self.name
