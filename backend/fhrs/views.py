from django.db.models import Q
from rest_framework import generics
from .models import Business
from .serializers import BusinessSerializer

class CoffeeShopListView(generics.ListAPIView):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        return Business.objects.filter(
            Q(business_type__icontains="cafe") | Q(business_type__icontains="coffee")
        )
