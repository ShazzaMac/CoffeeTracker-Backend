# --------------------------------------------------------
# this file contains the views for the Food Hygiene Rating data used in the application
#ref https://ratings.food.gov.uk/open-data-resources/documents/FHRS_APIv1_guidance_april24.pdf
# --------------------------------------------------------

from django.db.models import Q
from rest_framework import generics

from .models import Business
from .serializers import BusinessSerializer


class CoffeeShopListView(generics.ListAPIView):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        queryset = Business.objects.filter(
            Q(business_type__icontains="cafe") | Q(business_type__icontains="coffee")
        )

        # Gets the query parameters from the URL
        rating = self.request.query_params.get("rating", None)
        postcode = self.request.query_params.get("postcode", None)
        name = self.request.query_params.get("name", None)

        # Applies filters based on the query parameters
        if rating:
            queryset = queryset.filter(rating=rating)
        if postcode:
            queryset = queryset.filter(
                address__startswith=postcode[:4].upper()
            )  # Filter by postcode in address
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
