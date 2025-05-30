# ------------------------------------------
# This file contains the models for the Django application.
# It includes models for coffee shops, reviews, price records, and contact messages.
# ------------------------------------------

from django.db import models
from django.contrib.auth.models import User


# This model represents a coffee shop in the database - not yet in use
class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    website = models.URLField()
    social_media = models.URLField()
    image = models.ImageField(upload_to="shop_images/", null=True, blank=True)
    opening_times = models.TextField(null=True, blank=True)
    features = models.JSONField(
        null=True, blank=True
    )  # Store feature flags in a JSON format

    def __str__(self):
        return self.name


# This model represents a review for a coffee shop
class Review(models.Model):
    shop = models.ForeignKey(Shop, related_name="reviews", on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.shop.name}"

    # This model represents a price record for a coffee shop - used in the coffee tracker table
class PriceRecord(models.Model):
    shop = models.ForeignKey(
        Shop, related_name="price_records", on_delete=models.CASCADE
    )
    date = models.DateField()
    beverage = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    submitter_name = models.CharField(max_length=255)
    features = models.JSONField()  # Store the features like dogFriendly, wifi, etc.
    ratings = models.JSONField()  # Store the ratings in a JSON format

    def __str__(self):
        return f"{self.beverage} - {self.shop.name} - {self.date}"


# This model represents the result of processing the extracted data
class ShopResult(models.Model):
    json_data = models.TextField()  # Store the JSON data as a text field

    def __str__(self):
        return f"ShopResult {self.id}"


# This model represents a contact message sent by a user - about page
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    # This bit allows the data to be displayed in a more readable format
    def __str__(self):
        return self.name



# This model represents a leaderboard entry for the price guessing game
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    timestamp = models.DateTimeField(
        auto_now_add=True
    )  # Saves when entry is created but this is only viewable in the db

    class Meta:
        ordering = ["-points"]  # Shows highest scores first

    def __str__(self):
        return f"{self.user.username} - {self.points} - {self.timestamp}"
