# Description: This file contains tests for the FHRS API. Which as of tue 18th feb are all working

# things to test:
# - get all businesses
# - get a business by ID
# - get a business by name
# - get a business by rating
# - get a business by business type
# - get a business by address
# - get a business by latitude
# - get a business by longitude
# - get a business by multiple filters

#files to test include:
# - backend/fhrs/views.py
# - backend/fhrs/urls.py
# - backend/fhrs/serializers.py
# - backend/fhrs/models.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from fhrs.models import Business

class FHRSTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create test businesses in the database for use in all tests"""
        cls.business1 = Business.objects.create(
            id=1, name="Test Cafe", rating="5", business_type="Cafe",
            address="123 Test Street", latitude=1.0, longitude=1.0
            fhrs_id=some_valid_value  # Provide a valid value for fhrs_id

        )
        cls.business2 = Business.objects.create(
            id=2, name="Test Restaurant", rating="4", business_type="Restaurant",
            address="456 Food Avenue", latitude=2.0, longitude=2.0
            fhrs_id=some_valid_value  # Provide a valid value for fhrs_id

        )

    def test_fhrs_home(self):
        """Test the base FHRS API endpoint"""
        response = self.client.get(reverse("fhrs-home"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Hello, World!"})

    def test_get_all_businesses(self):
        """Test retrieving a list of all businesses"""
        response = self.client.get(reverse("fhrs-businesses"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_business_by_id(self):
        """Test retrieving a single business by ID"""
        response = self.client.get(reverse("fhrs-business-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)

    def test_get_business_by_invalid_id(self):
        """Test retrieving a business by an invalid ID should return 404"""
        response = self.client.get(reverse("fhrs-business-detail", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_business_by_name(self):
        """Test retrieving a business by its name"""
        response = self.client.get(reverse("fhrs-businesses"), {"name": "Test Cafe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["name"], "Test Cafe")

    def test_get_business_by_invalid_name(self):
        """Test retrieving a business by a non-existent name should return 404"""
        response = self.client.get(reverse("fhrs-businesses"), {"name": "Nonexistent"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_business_by_rating(self):
        """Test retrieving a business by rating"""
        response = self.client.get(reverse("fhrs-businesses"), {"rating": "5"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["rating"], "5")

    def test_get_business_by_business_type(self):
        """Test retrieving businesses by type (e.g., 'Cafe')"""
        response = self.client.get(reverse("fhrs-businesses"), {"business_type": "Cafe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["business_type"], "Cafe")

    def test_get_business_by_address(self):
        """Test retrieving a business by address"""
        response = self.client.get(reverse("fhrs-businesses"), {"address": "123 Test Street"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["address"], "123 Test Street")

    def test_get_business_by_coordinates(self):
        """Test retrieving a business by latitude and longitude"""
        response = self.client.get(reverse("fhrs-businesses"), {"latitude": 1.0, "longitude": 1.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["latitude"], 1.0)
        self.assertEqual(response.json()[0]["longitude"], 1.0)

    def test_get_business_by_multiple_filters(self):
        """Test retrieving a business by multiple filters (name, rating, type, etc.)"""
        response = self.client.get(reverse("fhrs-businesses"), {
            "name": "Test Cafe",
            "rating": "5",
            "business_type": "Cafe",
            "address": "123 Test Street",
            "latitude": 1.0,
            "longitude": 1.0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()[0]
        self.assertEqual(data["name"], "Test Cafe")
        self.assertEqual(data["rating"], "5")
        self.assertEqual(data["business_type"], "Cafe")
        self.assertEqual(data["address"], "123 Test Street")
        self.assertEqual(data["latitude"], 1.0)
        self.assertEqual(data["longitude"], 1.0)

    def test_get_business_by_invalid_filters(self):
        """Test retrieving businesses with invalid filters should return 404"""
        response = self.client.get(reverse("fhrs-businesses"), {
            "name": "Invalid", "rating": "Invalid", "business_type": "Invalid",
            "address": "Invalid", "latitude": "Invalid", "longitude": "Invalid"
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_business_by_partial_match(self):
        """Test retrieving businesses with partial name match (if supported)"""
        response = self.client.get(reverse("fhrs-businesses"), {"name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()) > 0)

    def test_get_business_with_pagination(self):
        """Test that the API supports pagination"""
        response = self.client.get(reverse("fhrs-businesses"), {"page": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())  # Check if paginated response format exists

    def test_get_business_with_invalid_page(self):
        """Test that requesting an invalid page returns an appropriate response"""
        response = self.client.get(reverse("fhrs-businesses"), {"page": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_businesses_by_query_param(self):
        """Test searching businesses using query params"""
        response = self.client.get(reverse("fhrs-businesses"), {"search": "Cafe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(b["name"] == "Test Cafe" for b in response.json()))

    def test_search_businesses_by_invalid_query(self):
        """Test searching businesses with invalid query returns 404"""
        response = self.client.get(reverse("fhrs-businesses"), {"search": "Nonexistent"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
