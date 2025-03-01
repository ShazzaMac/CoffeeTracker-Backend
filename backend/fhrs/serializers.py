from rest_framework import serializers

from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"  # You can modify this to only include specific fields

# In your view or serializer
def get_queryset(self):
    queryset = Business.objects.all()
    postcode = self.request.GET.get('postcode', None)
    if postcode:
        queryset = queryset.filter(address__icontains=postcode)  # Filter by postcode in address
    return queryset
