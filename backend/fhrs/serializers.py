# ------------------------------------------------------------------
# This file contains the serializers for the Food Hygiene Rating System (FHRS) app.
#ref https://ratings.food.gov.uk/open-data-resources/documents/FHRS_APIv1_guidance_april24.pdf
# ------------------------------------------------------------------

from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"  # Can be changed to specific fields if needed - to make irt more suitable for the coffee tracker app


def get_queryset(self):
    queryset = Business.objects.all()
    postcode = self.request.GET.get("postcode", None)
    if postcode:
        queryset = queryset.filter(
            address__icontains=postcode
        )  # Filter by postcode in address
    return queryset
