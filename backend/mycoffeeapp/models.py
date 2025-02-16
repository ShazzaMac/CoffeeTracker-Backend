# models.py
from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    website = models.URLField()
    social_media = models.URLField()
    image = models.ImageField(upload_to='shop_images/', null=True, blank=True)
    opening_times = models.TextField(null=True, blank=True)
    features = models.JSONField(null=True, blank=True)  # Store feature flags in a JSON format

class Review(models.Model):
    shop = models.ForeignKey(Shop, related_name='reviews', on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()

class PriceRecord(models.Model):
    shop = models.ForeignKey(Shop, related_name='price_records', on_delete=models.CASCADE)
    date = models.DateField()
    beverage = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    submitter_name = models.CharField(max_length=255)
    features = models.JSONField()  # Store the features like dogFriendly, wifi, etc.
    ratings = models.JSONField()  # Store the ratings in a JSON format
