# ------------------------------------------------------------------
# Django model for storing business information from the Food Hygiene Rating Scheme (FHRS)
# This data can then be used in the application to display information about locations and ratings
##ref https://ratings.food.gov.uk/open-data-resources/documents/FHRS_APIv1_guidance_april24.pdf
#  ------------------------------------------------------------------

from django.db import models


class Business(models.Model):
    fhrs_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    rating = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    business_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.rating}) - {self.address} - {self.business_type}"

    class Meta:
        pass
