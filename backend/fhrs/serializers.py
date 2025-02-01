from rest_framework import serializers

from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"  # You can modify this to only include specific fields
