from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from priceapp.models import PriceSubmission
from priceapp.serializers import PriceSubmissionSerializer
import json

class PriceTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.price = PriceSubmission.objects.create(
            establishment='Cafe Aroma',
            beverage='Latte',
            price=2.80,
            date='2024-03-27',
            submitter_name='Test User'
        )

    def test_price_list_view(self):
        response = self.client.get("/api/prices/")
        prices = PriceSubmission.objects.all()
        serializer = PriceSubmissionSerializer(prices, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_price_submission_view(self):
        data = {
            "establishment": "Brew Bros",
            "beverage": "Flat White",
            "price": "2.80",
            "date": "2024-03-27",
            "submitterName": "Alex Test",
            "features": {
                "dogFriendly": True,
                "wifi": False,
                "outdoorSeating": False,
                "plantMilks": True,
                "brunchLunch": False,
                "wheelchairAccess": True
            },
            "ratings": {
                "coffeeTaste": 5,
                "coffeeOptions": 4,
                "service": 5,
                "atmosphere": 3,
                "valueForMoney": 4
            }
        }

        response = self.client.post(
            "/api/submit-price/",
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PriceSubmission.objects.count(), 2)
        new_price = PriceSubmission.objects.last()
        self.assertEqual(new_price.establishment, "Brew Bros")

    def test_submit_price_invalid_data(self):
        data = {
            "establishment": "",
            "beverage": "Espresso",
            "price": "not-a-number",
            "date": "2024-03-27",
            "submitterName": "Bad User",
            "features": {
                "dogFriendly": False,
                "wifi": False,
                "outdoorSeating": False,
                "plantMilks": False,
                "brunchLunch": False,
                "wheelchairAccess": False
            },
            "ratings": {
                "coffeeTaste": 3,
                "coffeeOptions": 3,
                "service": 3,
                "atmosphere": 3,
                "valueForMoney": 3
            }
        }

        response = self.client.post(
            "/api/submit-price/",
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
