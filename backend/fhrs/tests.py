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

# Unit test for the FHRS API

class FHRSTestCase(TestCase):
    def test_fhrs(self):
        response = self.client.get('/fhrs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})

        # Unit test to check if the API returns a list of businesses
    def test_fhrs_businesses(self):
        response = self.client.get('/fhrs/businesses/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

        # Unit test to check if the API returns a business by ID
    def test_fhrs_business_by_id(self):
        response = self.client.get('/fhrs/businesses/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)

        # Unit test to check if the API returns a business by name
    def test_fhrs_business_by_name(self):
        response = self.client.get('/fhrs/businesses/?name=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], 'Test')

        # Unit test to check if the API returns a business by rating
    def test_fhrs_business_by_rating(self):
        response = self.client.get('/fhrs/businesses/?rating=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['rating'], '5')

        # Unit test to check if the API returns a business by business type
    def test_fhrs_business_by_business_type(self):
        response = self.client.get('/fhrs/businesses/?business_type=Cafe')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['business_type'], 'Cafe')

        # Unit test to check if the API returns a business by address
    def test_fhrs_business_by_address(self):
        response = self.client.get('/fhrs/businesses/?address=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['address'], 'Test')

        # Unit test to check if the API returns a business by latitude
    def test_fhrs_business_by_latitude(self):
        response = self.client.get('/fhrs/businesses/?latitude=1.0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['latitude'], 1.0)

        # Unit test to check if the API returns a business by longitude
    def test_fhrs_business_by_longitude(self):
        response = self.client.get('/fhrs/businesses/?longitude=1.0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['longitude'], 1.0)

        # Unit test to check if the API returns a business by multiple filters
    def test_fhrs_business_by_multiple_filters(self):
        response = self.client.get('/fhrs/businesses/?name=Test&rating=5&business_type=Cafe&address=Test&latitude=1.0&longitude=1.0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], 'Test')
        self.assertEqual(response.json()[0]['rating'], '5')
        self.assertEqual(response.json()[0]['business_type'], 'Cafe')
        self.assertEqual(response.json()[0]['address'], 'Test')
        self.assertEqual(response.json()[0]['latitude'], 1.0)
        self.assertEqual(response.json()[0]['longitude'], 1.0)

        # Unit test to check if the API returns a business by invalid ID
    def test_fhrs_business_by_invalid_id(self):
        response = self.client.get('/fhrs/businesses/1000/')
        self.assertEqual(response.status_code, 404)

        # Unit test to check if the API returns a business by invalid name
    def test_fhrs_business_by_invalid_name(self):
        response = self.client.get('/fhrs/businesses/?name=Invalid')
        self.assertEqual(response.status_code, 404)

        # Unit test to check if the API returns a business by invalid rating
    def test_fhrs_business_by_invalid_rating(self):
        response = self.client.get('/fhrs/businesses/?rating=Invalid')
        self.assertEqual(response.status_code, 404)

        # Unit test to check if the API returns a business by invalid business type
    def test_fhrs_business_by_invalid_business_type(self):
        response = self.client.get('/fhrs/businesses/?business_type=Invalid')
        self.assertEqual(response.status_code, 404)

        # Unit test to check if the API returns a business by invalid address
    def test_fhrs_business_by_invalid_address(self):
        response = self.client.get('/fhrs/businesses/?address=Invalid')
        self.assertEqual(response.status_code, 404)

        # Unit test to check if the API returns a business by invalid latitude
    def test_fhrs_business_by_invalid_latitude(self):
        response = self.client.get('/fhrs/businesses/?latitude=Invalid')
        self.assertEqual(response.status_code, 404)

        # Unit test to check if the API returns a business by invalid longitude
    def test_fhrs_business_by_invalid_longitude(self):
        response = self.client.get('/fhrs/businesses/?longitude=Invalid')
        self.assertEqual(response.status_code, 404)

        # Unit test to check if the API returns a business by invalid filters
    def test_fhrs_business_by_invalid_filters(self):
        response = self.client.get('/fhrs/businesses/?name=Invalid&rating=Invalid&business_type=Invalid&address=Invalid&latitude=Invalid&longitude=Invalid')
        self.assertEqual(response.status_code, 404)


        
       


