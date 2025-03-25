# ocrapp/tests.py
# this test now passes successfully --- as of 25/03/25
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class OCRExtractEndpointTest(TestCase):
    def test_no_file_uploaded_returns_error(self):
        """
        Ensure the /ocr-extract/ endpoint returns 400 if no file is uploaded.
        """
        response = self.client.post('/api/ocr-extract/')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
