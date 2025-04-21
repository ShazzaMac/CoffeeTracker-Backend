# +-----------------------------------------------------+
#  This file holds the serializers for the main part
# f the app. It turns models into json objects so they can be
#  easily sent and received by the frontend.
# +-----------------------------------------------------+

from rest_framework import serializers
from .models import Shop, Review, PriceRecord, Leaderboard


from rest_framework import serializers
from .models import Leaderboard


# this serializer is used to convert the Leaderboard model into a JSON object
class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Leaderboard
        fields = ["username", "points"]


# this serializer is used to convert the Review model into a JSON object
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["user", "rating", "comment"]


# this serializer is used to convert the PriceRecord model into a JSON object
class PriceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRecord
        fields = ["date", "beverage", "price", "submitter_name", "features", "ratings"]


# this serializer is used to convert the Shop model into a JSON object - it is yet to be implemented
class ShopSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    price_records = PriceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = [
            "name",
            "address",
            "website",
            "social_media",
            "image",
            "opening_times",
            "features",
            "reviews",
            "price_records",
        ]
