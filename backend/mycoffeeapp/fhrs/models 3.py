from django.db import models

# Create your models here.
from django.db import models

class Business(models.Model):
    fhrs_id = models.IntegerField(unique=True)  # Unique ID from FHRS
    name = models.CharField(max_length=255)
    address = models.TextField()
    rating = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    business_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.rating})"
