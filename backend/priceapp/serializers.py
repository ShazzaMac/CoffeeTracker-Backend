from rest_framework import serializers
from .models import PriceSubmission

class PriceSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceSubmission
        fields = "__all__"
