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