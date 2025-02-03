#files to test include:
# - backend/fhrs/views.py
# - backend/fhrs/urls.py
# - backend/fhrs/serializers.py
# - backend/fhrs/models.py

from django.test import TestCase

# unit test for the API
class APITestCase(TestCase):
    def test_api(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})

        # unit test to check if the API returns a list of businesses
    def test_api_businesses(self):
        response = self.client.get('/api/businesses/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

        # unit test to check if the API returns a business by ID
    def test_api_business_by_id(self):
        response = self.client.get('/api/businesses/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)

        # unit test to check if the API returns a business by name
    def test_api_business_by_name(self):
        response = self.client.get('/api/businesses/?name=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], 'Test')

        # unit test to check if the API returns a business by rating
    def test_api_business_by_rating(self):
        response = self.client.get('/api/businesses/?rating=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['rating'], '5')



