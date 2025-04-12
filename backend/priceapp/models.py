from django.db import models

class PriceSubmission(models.Model):
    establishment = models.CharField(max_length=255)
    date = models.DateField()
    beverage = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    submitter_name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.beverage:
            self.beverage = self.beverage.strip().title()  # Converts "latte" -> "Latte"
        super().save(*args, **kwargs)

    # Features as Boolean Fields
    dog_friendly = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    outdoor_seating = models.BooleanField(default=False)
    plant_milks = models.BooleanField(default=False)
    brunch_lunch = models.BooleanField(default=False)
    wheelchair_access = models.BooleanField(default=False)

    # Ratings
    coffee_taste = models.IntegerField(default=0)
    coffee_options = models.IntegerField(default=0)
    service = models.IntegerField(default=0)
    atmosphere = models.IntegerField(default=0)
    value_for_money = models.IntegerField(default=0)

    # File Upload
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)

    def __str__(self):
        return f"{self.establishment} - {self.beverage} (£{self.price})"
