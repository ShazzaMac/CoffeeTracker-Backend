# -----------------------------------------------------------------
# This file contains test cases for the PriceSubmission model and its API endpoints.
# It uses Django's TestCase and APITestCase classes to create unit tests for the model and API views.
# It includes tests for creating, retrieving, and validating price submissions.
# references: https://docs.djangoproject.com/en/5.2/topics/testing/overview/
# references:https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing
# -----------------------------------------------------------------

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from priceapp.models import PriceSubmission
from priceapp.serializers import PriceSubmissionSerializer
import json
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase


class PriceSubmissionViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/submit-price/"
        self.valid_data = {
            "establishment": "Caffeine Corner",
            "date": "2024-03-25",
            "beverage": "Latte",
            "price": "3.50",
            "submitterName": "Test User",
            "features": {
                "dogFriendly": True,
                "wifi": False,
                "outdoorSeating": True,
                "plantMilks": True,
                "brunchLunch": False,
                "wheelchairAccess": True,
            },
            "ratings": {
                "coffeeTaste": 4,
                "coffeeOptions": 5,
                "service": 3,
                "atmosphere": 4,
                "valueForMoney": 4,
            },
        }

    # tests svalid submission with all required fields
    def test_post_valid_submission(self):
        response = self.client.post(
            self.url, data=json.dumps(self.valid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PriceSubmission.objects.count(), 1)

    # Tests submission with completely empty data
    def test_post_missing_form_data(self):
        response = self.client.post(
            self.url, data={}, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)

    # tests submission with invalid JSON payload
    def test_post_invalid_json(self):
        response = self.client.post(
            self.url, data="{invalid-json}", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    # Tests form submission with missing required fields (establishment removed)
    def test_post_missing_fields(self):
        incomplete_data = self.valid_data.copy()
        del incomplete_data["establishment"]
        response = self.client.post(
            self.url, data=json.dumps(incomplete_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    # Tests GET request to fetch all submissions
    def test_get_all_submissions(self):
        PriceSubmission.objects.create(
            establishment="Cafe A",
            date="2024-01-01",
            beverage="Espresso",
            price=2.50,
            submitter_name="Alice",
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # Tests file upload alongside valid formData
    def test_post_with_file_upload(self):
        file = SimpleUploadedFile(
            "receipt.jpg", b"file_content", content_type="image/jpeg"
        )
        payload = {
            "formData": json.dumps(self.valid_data),
        }
        response = self.client.post(self.url, data={"file": file, **payload})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Tests form submission with extreme (but valid) price values
    def test_post_extreme_values(self):
        extreme_data = self.valid_data.copy()
        extreme_data["price"] = "99.99"
        response = self.client.post(
            self.url, data=json.dumps(extreme_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test if boolean strings like "true"/"false" are accepted
    def test_post_string_boolean_flags(self):
        data = self.valid_data.copy()
        data["features"] = {
            k: "true" if v else "false" for k, v in data["features"].items()
        }
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PriceSubmission.objects.count(), 1)

    # Tests submission missing formData in a multipart request
    def test_post_multipart_missing_formData(self):
        client = APIClient()
        file = SimpleUploadedFile(
            "receipt.jpg", b"file_content", content_type="image/jpeg"
        )
        response = client.post(
            self.url, data={"file": file}, format="multipart"  # No 'formData' field
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("formData is missing", response.json().get("error", ""))

    # Tests invalid formData JSON inside multipart
    def test_post_multipart_invalid_json(self):
        client = APIClient()
        invalid_form_data = "{invalid: json]"
        file = SimpleUploadedFile(
            "receipt.jpg", b"file_content", content_type="image/jpeg"
        )
        response = client.post(
            self.url,
            data={"file": file, "formData": invalid_form_data},
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid form data JSON", response.json().get("error", ""))


class PriceTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.price = PriceSubmission.objects.create(
            establishment="Cafe Aroma",
            beverage="Latte",
            price=2.80,
            date="2024-03-27",
            submitter_name="Test User",
        )

    # Tests GET view for all price entries
    def test_price_list_view(self):
        response = self.client.get("/api/prices/")
        prices = PriceSubmission.objects.all()
        serializer = PriceSubmissionSerializer(prices, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # Tests successful price submission via POST
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
                "wheelchairAccess": True,
            },
            "ratings": {
                "coffeeTaste": 5,
                "coffeeOptions": 4,
                "service": 5,
                "atmosphere": 3,
                "valueForMoney": 4,
            },
        }

        response = self.client.post(
            "/api/submit-price/", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PriceSubmission.objects.count(), 2)
        new_price = PriceSubmission.objects.last()
        self.assertEqual(new_price.establishment, "Brew Bros")

    # Tests invalid price submission (invalid types, missing values)
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
                "wheelchairAccess": False,
            },
            "ratings": {
                "coffeeTaste": 3,
                "coffeeOptions": 3,
                "service": 3,
                "atmosphere": 3,
                "valueForMoney": 3,
            },
        }

        response = self.client.post(
            "/api/submit-price/", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Tests the submission missing the nested 'ratings' field
    def test_post_missing_required_fields(self):
        incomplete_data = {
            "establishment": "Cafe Coverage",
            "date": "2024-04-01",
            "beverage": "Flat White",
            "price": "3.90",
            "submitterName": "Test User",
            "features": {
                "dogFriendly": True,
                "wifi": True,
                "outdoorSeating": True,
                "plantMilks": True,
                "brunchLunch": True,
                "wheelchairAccess": True,
            },
            # 'ratings' missing on purpose
        }

        response = self.client.post(
            "/api/submit-price/",
            data=json.dumps(incomplete_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    # test for submitting the same data twice
    def test_duplicate_submission(self):
        self.client.post(
            self.url, data=json.dumps(self.valid_data), content_type="application/json"
        )
        response = self.client.post(
            self.url, data=json.dumps(self.valid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)  # Or 400 if duplicates are blocked

    # Tests if invalid boolean strings (e.g., "yes") are accepted or converted
    def test_invalid_boolean_strings(self):
        data = self.valid_data.copy()
        data["features"] = {k: "yes" for k in data["features"].keys()}
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    # tests if missing 'ratings' key results in an error
    def test_missing_ratings_key(self):
        data = self.valid_data.copy()
        del data["ratings"]
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    # Tests if a valid multipart request with formData string is accepted
    def test_multipart_valid_formdata_string(self):
        file = SimpleUploadedFile(
            "receipt.jpg", b"file_content", content_type="image/jpeg"
        )
        form_data = json.dumps(self.valid_data)
        response = self.client.post(
            self.url, data={"file": file, "formData": form_data}
        )
        self.assertEqual(response.status_code, 201)
