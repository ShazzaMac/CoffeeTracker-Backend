from rest_framework import serializers
from .models import PriceSubmission

class PriceSubmissionSerializer(serializers.ModelSerializer):
    # Rename submitter_name to submitterName
    submitterName = serializers.CharField(source="submitter_name")
    # Nest the ratings fields into one object
    ratings = serializers.SerializerMethodField()
    # Nest the feature fields into one object
    features = serializers.SerializerMethodField()
    
    class Meta:
        model = PriceSubmission
        fields = [
            'id',
            'establishment',
            'date',
            'beverage',
            'price',
            'submitterName',
            'ratings',
            'features',
            'receipt',  # Add receipt field to the serializer
        ]
    
    def get_ratings(self, obj):
        return {
            "coffeeTaste": obj.coffee_taste,
            "coffeeOptions": obj.coffee_options,
            "service": obj.service,
            "atmosphere": obj.atmosphere,
            "valueForMoney": obj.value_for_money,
        }
    
    def get_features(self, obj):
        return {
            "dogFriendly": obj.dog_friendly,
            "wifi": obj.wifi,
            "outdoorSeating": obj.outdoor_seating,
            "plantMilks": obj.plant_milks,
            "brunchLunch": obj.brunch_lunch,
            "wheelchairAccess": obj.wheelchair_access,
        }
