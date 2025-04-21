#--------------------------------------------------------------------------------
# PriceSubmission Serializer 
#--------------------------------------------------------------------------------

from rest_framework import serializers
from .models import PriceSubmission

class PriceSubmissionSerializer(serializers.ModelSerializer):
    submitterName = serializers.CharField(source="submitter_name")
    ratings = serializers.SerializerMethodField()
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
            'receipt', 
        ]
    
    # This method is used to convert the ratings field into a JSON object
    # It takes the ratings from the model and converts them into a dictionary
    # with the keys being the rating names and the values being the rating values
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
