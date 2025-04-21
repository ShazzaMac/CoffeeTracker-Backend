# +-----------------------------------------------------+
# CoffeeApp Tests
# +-----------------------------------------------------+


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from mycoffeeapp.models import (
    Shop,
    Review,
    PriceRecord,
    ContactMessage,
    ShopResult,
    Leaderboard,
)
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


# tests the string representation of the Shop model
class CoffeeAppModelTests(TestCase):
    def test_shop_str(self):
        shop = Shop.objects.create(
            name="Café Bliss",
            address="123 Main St",
            website="https://example.com",
            social_media="https://instagram.com/example",
        )
        self.assertEqual(str(shop), "Café Bliss")

    # Tests the string representation of the Review model
    def test_review_str(self):
        shop = Shop.objects.create(
            name="Café Bliss",
            address="123 Main St",
            website="https://example.com",
            social_media="https://instagram.com/example",
        )
        review = Review.objects.create(
            shop=shop, user="Alice", rating=5, comment="Excellent!"
        )
        self.assertEqual(str(review), "Alice - Café Bliss")

    # Tests the string representation of the PriceRecord model
    def test_price_record_str(self):
        shop = Shop.objects.create(
            name="Beanery",
            address="456 High St",
            website="https://beanery.com",
            social_media="https://facebook.com/beanery",
        )
        record = PriceRecord.objects.create(
            shop=shop,
            date="2024-03-01",
            beverage="Latte",
            price=3.20,
            submitter_name="Bob",
            features={},
            ratings={},
        )
        self.assertIn("Latte - Beanery", str(record))

    # Tests the string representation of the ContactMessage model
    def test_contact_message_str(self):
        msg = ContactMessage.objects.create(
            name="Charlie", email="charlie@example.com", message="Hello!"
        )
        self.assertEqual(str(msg), "Charlie")

    # Tests the string representation of the ShopResult model
    def test_shop_result_str(self):
        result = ShopResult.objects.create(json_data='{"data": true}')
        self.assertIn("ShopResult", str(result))

    # Tests the string representation of the Leaderboard model
    def test_leaderboard_str(self):
        user = User.objects.create_user(username="testuser", password="pass")
        entry = Leaderboard.objects.create(user=user, points=100)
        self.assertIn("testuser", str(entry))


# tests user and authentication for protected endpoints
class CoffeeAppViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.client.force_authenticate(user=self.user)

    # Tests the leaderboard list view
    def test_leaderboard_list(self):
        Leaderboard.objects.create(user=self.user, points=10)
        response = self.client.get("/api/leaderboard/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json()[0])

    # Tests the leaderboard update view
    def test_update_leaderboard_success(self):
        response = self.client.post(
            "/api/update-leaderboard/", {"points": 50}, format="json"
        )
        self.assertEqual(response.status_code, 201)

    # Tests the leaderboard update view with missing points
    def test_update_leaderboard_missing_points(self):
        response = self.client.post("/api/update-leaderboard/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    # Tests the CSRF token view
    def test_csrf_token_view(self):
        response = self.client.get("/api/csrf/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrfToken", response.json())

    # Tests submitting a price
    def test_contact_form_success(self):
        response = self.client.post(
            "/api/contact/",
            data=json.dumps(
                {"name": "Alice", "email": "alice@example.com", "message": "Hi there"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    # Tests the contact form with missing fields
    def test_contact_form_missing_fields(self):
        response = self.client.post(
            "/api/contact/",
            data=json.dumps({"name": "", "email": "test@example.com", "message": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    # below tests sending a GET request to the contact form (should be invalid
    def test_contact_form_get_method(self):
        response = self.client.get("/api/contact/")
        self.assertEqual(response.status_code, 400)

    # Tests retrieving user profile when authenticated
    def test_user_profile_authenticated(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "user1")

    # Tests retrieving user profile when unauthenticated
    def test_user_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, 401)

    # tests the upload with an unsupported file type
    def test_upload_file_invalid_type(self):
        fake_file = SimpleUploadedFile(
            "test.doc", b"content", content_type="text/plain"
        )
        response = self.client.post("/api/upload/", {"file": fake_file})
        self.assertEqual(response.status_code, 400)

    # tests saving OCR extracted data with missing fields
    def test_save_extracted_data_missing_fields(self):
        response = self.client.post(
            "/api/save-extracted-data/",
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertIn(response.status_code, [400, 500])

    # Tests custom test endpoint with a POST request
    def test_my_view_post_success(self):
        response = self.client.post("/api/test-post/")
        self.assertEqual(response.status_code, 200)

    # Test that GET requests to test endpoint return an error
    def test_my_view_get_invalid(self):
        response = self.client.get("/api/test-post/")
        self.assertEqual(response.status_code, 400)

    # Tests alternate CSRF token endpoints return a valid token
    def test_alternative_csrf_token_routes(self):
        for url in ["/csrf-token/", "/api/csrf-token/"]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn("csrf_token", response.json())
