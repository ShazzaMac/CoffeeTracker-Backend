from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from priceapp.models import Product, Price
from django.utils import timezone

class ProductModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product_name = "Test Product"
        cls.product = Product.objects.create(name=cls.product_name)

    def test_model_can_create_a_product(self):
        old_count = Product.objects.count()
        Product.objects.create(name="New Product")
        new_count = Product.objects.count()
        self.assertNotEqual(old_count, new_count)

class ProductViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.product = Product.objects.create(name="Test Product")

    def test_api_can_create_a_product(self):
        response = self.client.post(
            reverse('product-create'),
            {'name': 'New Product'},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_product(self):
        response = self.client.get(
            reverse('product-detail', kwargs={'pk': self.product.id}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_api_can_update_product(self):
        response = self.client.put(
            reverse('product-detail', kwargs={'pk': self.product.id}),
            {'name': 'Updated Product'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_product(self):
        response = self.client.delete(
            reverse('product-detail', kwargs={'pk': self.product.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class PriceModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name="Test Product")
        cls.price = Price.objects.create(product=cls.product, price=100, date=timezone.now())

    def test_model_can_create_a_price(self):
        old_count = Price.objects.count()
        Price.objects.create(product=self.product, price=200, date=timezone.now())
        new_count = Price.objects.count()
        self.assertNotEqual(old_count, new_count)

class PriceViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.product = Product.objects.create(name="Test Product")
        cls.price = Price.objects.create(product=cls.product, price=100, date=timezone.now())

    def test_api_can_create_a_price(self):
        response = self.client.post(
            reverse('price-create'),
            {'product': self.product.id, 'price': 200, 'date': timezone.now()},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_price(self):
        response = self.client.get(
            reverse('price-detail', kwargs={'pk': self.price.id}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], self.price.price)

    def test_api_can_update_price(self):
        response = self.client.put(
            reverse('price-detail', kwargs={'pk': self.price.id}),
            {'product': self.product.id, 'price': 300, 'date': timezone.now()},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_price(self):
        response = self.client.delete(
            reverse('price-detail', kwargs={'pk': self.price.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_can_get_all_prices(self):
        response = self.client.get(
            reverse('price-list'),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    class PriceSubmissionViewExtraTests(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.url = "/api/submit-price/"
            self.valid_data = {
            "establishment": "Caffeine Corner",
            "date": "2024-03-25",
            "beverage": "Latte",
            "price": "3.50",
            "submitterName": "Test User",
            "features": {
                "dogFriendly": "true",
                "wifi": "false",
                "outdoorSeating": "true",
                "plantMilks": "true",
                "brunchLunch": "false",
                "wheelchairAccess": "true"
            },
            "ratings": {
                "coffeeTaste": 4,
                "coffeeOptions": 5,
                "service": 3,
                "atmosphere": 4,
                "valueForMoney": 4
            }
        }

    def test_post_missing_formData_key(self):
        # Simulate missing `formData` key in multipart request
        response = self.client.post(self.url, data={}, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 400)
        self.assertIn("formData is missing", response.data.get("error", ""))

    def test_post_invalid_json_format(self):
        # Invalid JSON string
        response = self.client.post(self.url, data={"formData": "{invalid-json}"}, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid form data JSON", response.data.get("error", ""))

    def test_post_valid_data_with_file(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        file = SimpleUploadedFile("receipt.jpg", b"fake-content", content_type="image/jpeg")
        payload = {
            "formData": json.dumps(self.valid_data),
            "file": file
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_all_price_submissions(self):
        # Ensure GET request works
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_str_to_bool_helper(self):
        from priceapp.views import str_to_bool
        self.assertTrue(str_to_bool("true"))
        self.assertFalse(str_to_bool("false"))
        self.assertTrue(str_to_bool(True))
        self.assertFalse(str_to_bool(False))
