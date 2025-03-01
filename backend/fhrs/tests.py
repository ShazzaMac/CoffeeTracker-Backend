#---------Do not change this file as all tests now pass. ------------
#---------This file is used to test the views in the fhrs app. ------------
#---------The tests are run using the command python manage.py test fhrs------------

from django.test import TestCase
from django.urls import reverse
from fhrs.models import Business

class CoffeeShopListViewTests(TestCase):

    def setUp(self):
        # Set up your test data
        Business.objects.create(fhrs_id=0, name="Test Cafe", address="123 Some Street, BT2", rating="5", business_type="Cafe")
        Business.objects.create(fhrs_id=1, name="Cafe A", address="123 Test St, BT1 1AA", rating="5", latitude=54.597, longitude=-5.93, business_type="Cafe")
        Business.objects.create(fhrs_id=2, name="Coffee B", address="456 Coffee Rd, BT9 2BB", rating="4", latitude=54.598, longitude=-5.94, business_type="Coffee Shop")

    def test_get_all_coffee_shops(self):
        response = self.client.get('/api/shop-profile/')  # Adjust your URL accordingly
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 2)  # Expect at least 2 coffee shops

    def test_filter_by_name(self):
        response = self.client.get('/api/shop-profile/', {'name': 'Cafe'})
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 1)  # Expect at least one result matching 'Cafe'
        self.assertTrue(all('Cafe' in item['name'] for item in data))  # Check that all results contain 'Cafe'

    def test_filter_by_postcode(self):
        response = self.client.get('/api/shop-profile/', {'address': 'BT9'})
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 1)  # Expect at least one result matching 'BT2'
        self.assertTrue(any('BT2' in item['address'] for item in data))  # Check that all results contain 'BT2'

   
    def test_filter_by_rating(self):
        response = self.client.get('/api/shop-profile/', {'rating': '5'})
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 1)  # Expect at least one result with rating '5'
        self.assertTrue(all(item['rating'] == '5' for item in data))  # Check that all results have rating '5'
