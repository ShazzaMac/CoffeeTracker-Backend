# serializers.py
from rest_framework import serializers
from .models import Shop, Review, PriceRecord, Leaderboard


from rest_framework import serializers
from .models import Leaderboard

class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['username', 'points']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment']

class PriceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRecord
        fields = ['date', 'beverage', 'price', 'submitter_name', 'features', 'ratings']

class ShopSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    price_records = PriceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ['name', 'address', 'website', 'social_media', 'image', 'opening_times', 'features', 'reviews', 'price_records']
