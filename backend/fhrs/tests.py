# -----------------------------------------------------------
# tests to ensure that the coffee shop list view works correctly
# and that filtering by name, address, and rating works as expected.
# references: https://docs.djangoproject.com/en/5.2/topics/testing/overview/
# references:https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing
# #-----------------------------------------------------------
from django.test import TestCase
from fhrs.models import Business


class CoffeeShopListViewTests(TestCase):

    def setUp(self):
        Business.objects.create(
            fhrs_id=0,
            name="Test Cafe",
            address="123 Some Street, BT2",
            rating="5",
            business_type="Cafe",
        )
        Business.objects.create(
            fhrs_id=1,
            name="Cafe A",
            address="123 Test St, BT1 1AA",
            rating="5",
            latitude=54.597,
            longitude=-5.93,
            business_type="Cafe",
        )
        # Updated this line so address starts with "BT9"
        Business.objects.create(
            fhrs_id=2,
            name="Coffee B",
            address="BT9 2BB, 456 Coffee Rd",
            rating="4",
            latitude=54.598,
            longitude=-5.94,
            business_type="Coffee Shop",
        )

        # Test to ensure that all coffee shops are returned

    def test_get_all_coffee_shops(self):
        response = self.client.get("/shop-profile/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 2)

        # Test to ensure that filtering by name returns the correct results

    def test_filter_by_name(self):
        response = self.client.get("/shop-profile/", {"name": "Cafe"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 1)
        self.assertTrue(all("Cafe" in item["name"] for item in data))

        # Test to ensure that filtering by address returns the correct results

    def test_filter_by_postcode(self):
        response = self.client.get("/shop-profile/", {"postcode": "BT9"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 1)
        self.assertTrue(any("BT9" in item["address"] for item in data))

        # Test to ensure that filtering by rating returns the correct results

    def test_filter_by_rating(self):
        response = self.client.get("/shop-profile/", {"rating": "5"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertGreaterEqual(len(data), 1)
        self.assertTrue(all(item["rating"] == "5" for item in data))
