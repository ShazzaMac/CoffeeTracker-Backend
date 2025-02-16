from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CoffeeShop

CustomUser = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_email_unique(self):
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username='testuser2',
                email='testuser@example.com',
                password='testpass123',
                first_name='Test2',
                last_name='User2'
            )

class CoffeeShopModelTest(TestCase):
    def setUp(self):
        self.coffee_shop = CoffeeShop.objects.create(
            name='Test Coffee Shop',
            location='123 Test St',
            average_price=3.50,
            rating=4.5,
            most_popular_coffee='Latte'
        )

    def test_coffee_shop_creation(self):
        self.assertEqual(self.coffee_shop.name, 'Test Coffee Shop')
        self.assertEqual(self.coffee_shop.location, '123 Test St')
        self.assertEqual(self.coffee_shop.average_price, 3.50)
        self.assertEqual(self.coffee_shop.rating, 4.5)
        self.assertEqual(self.coffee_shop.most_popular_coffee, 'Latte')

    def test_coffee_shop_str(self):
        self.assertEqual(str(self.coffee_shop), 'Test Coffee Shop')