from rest_framework import serializers
from .models import PriceSubmission

class PriceSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceSubmission
        fields = "__all__"

def create(self, validated_data):
    validated_data['submitter'] = self.context['request'].user
    return super().create(validated_data)
