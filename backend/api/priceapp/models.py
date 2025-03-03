from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings

class PriceSubmission(models.Model):
    establishment = models.CharField(max_length=255)
    date = models.DateField()
    beverage = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    features = models.JSONField()  # stores dogFriendly, wifi, etc.
    ratings = models.JSONField()   # stores coffeeTaste, service, etc.

    # File Upload
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)

    def __str__(self):
        return f"{self.establishment} - {self.beverage} (£{self.price})"
