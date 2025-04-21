# -------------------------------------------------------
# These tests are for the OCR app, which handles image processing and text extraction.
# This test now passes successfully --- as of 25/03/25
# Additional coverage tested - 30/03/25
# -------------------------------------------------------

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os
import unittest
from unittest.mock import patch, MagicMock
from api.ocrapp import utils
import numpy as np


class OCRUtilsTests(unittest.TestCase):

    # Tests that valid file extensions are accepted
    def test_allowed_file_valid(self):
        self.assertTrue(utils.allowed_file("receipt.jpg"))
        self.assertTrue(utils.allowed_file("file.PDF"))

    # Tests that invalid file extensions are rejected
    def test_allowed_file_invalid(self):
        self.assertFalse(utils.allowed_file("file.exe"))

    # Simulates successful conversion from HEIC to JPG
    @patch("subprocess.run")
    def test_convert_heic_to_jpg_success(self, mock_run):
        mock_run.return_value = MagicMock()
        with patch("os.path.exists", return_value=True):
            result = utils.convert_heic_to_jpg("test.heic")
            self.assertTrue(result.endswith(".jpg"))

    # Simulates failure during HEIC to JPG conversion
    @patch("subprocess.run", side_effect=Exception("fail"))
    def test_convert_heic_to_jpg_failure(self, mock_run):
        result = utils.convert_heic_to_jpg("test.heic")
        self.assertIsNone(result)

    # Ensures exception is handled properly in HEIC conversion
    @patch("subprocess.run", side_effect=Exception("conversion failed"))
    def test_convert_heic_to_jpg_handles_exception(self, mock_run):
        result = utils.convert_heic_to_jpg("sample.heic")
        self.assertIsNone(result)

    # Simulates Tesseract returning no text and checks error handling
    @patch("api.ocrapp.utils.pytesseract.image_to_string", return_value="   ")
    @patch("api.ocrapp.utils.preprocess_image", return_value="dummy.png")
    @patch("PIL.Image.open")
    def test_extract_text_no_text(self, mock_image, mock_preprocess, mock_ocr):
        result = utils.extract_text("dummy.jpg")
        self.assertEqual(result, "Error: No text found in OCR.")

    # This simulates a crash in preprocessing and checks error response
    @patch("api.ocrapp.utils.preprocess_image", side_effect=Exception("crash"))
    def test_extract_text_generic_exception(self, mock_preprocess):
        result = utils.extract_text("crash.jpg")
        self.assertIn("Error processing file", result)

    # Simulates an empty PDF and ensures correct error message
    @patch("api.ocrapp.utils.convert_from_path", return_value=[])
    def test_extract_text_empty_pdf(self, mock_convert):
        result = utils.extract_text("empty.pdf")
        self.assertEqual(result, "Error: No images found in PDF.")

    # Mocks EasyOCR and checks if text is correctly extracted
    @patch("easyocr.Reader")
    def test_easyocr_extract_text(self, mock_reader_class):
        mock_reader = MagicMock()
        mock_reader.readtext.return_value = ["Latte", "3.00"]
        mock_reader_class.return_value = mock_reader
        text = utils.easyocr_extract_text("sample.jpg")
        self.assertIn("Latte", text)

    # And this ensures preprocessed image file is saved successfully
    @patch("cv2.imread")
    @patch("cv2.filter2D")
    @patch("cv2.imwrite")
    @patch("os.path.exists", return_value=True)
    def test_preprocess_image_saves_file(
        self, mock_exists, mock_imwrite, mock_filter2D, mock_imread
    ):
        mock_imread.return_value = MagicMock()
        mock_filter2D.return_value = MagicMock()
        result = utils.preprocess_image("sample.jpg")
        self.assertIn("_preprocessed.png", result)

    # Checks behavior when image save fails but path still returns
    @patch("cv2.imread", return_value=np.zeros((100, 100), dtype=np.uint8))
    @patch("cv2.filter2D", return_value=np.zeros((100, 100), dtype=np.uint8))
    @patch("cv2.imwrite", return_value=False)
    @patch("os.path.exists", return_value=False)
    def test_preprocess_image_save_failure(
        self, mock_exists, mock_imwrite, mock_filter2D, mock_imread
    ):
        result = utils.preprocess_image("fail_save.jpg")
        self.assertIn("_preprocessed.png", result)

    # Simulates Tesseract OCR flow and checks extracted content
    @patch("api.ocrapp.utils.preprocess_image")
    @patch("pytesseract.image_to_string")
    def test_extract_text_with_tesseract(self, mock_ocr, mock_preprocess):
        mock_ocr.return_value = "Latte \u00a33.00"
        mock_preprocess.return_value = "sample_preprocessed.png"
        with patch("PIL.Image.open"):  # mock Image.open
            result = utils.extract_text("sample.jpg")
        self.assertIn("Latte", result)

    # Simulates EasyOCR flow and checks extracted content
    @patch("api.ocrapp.utils.preprocess_image")
    @patch("api.ocrapp.utils.easyocr_extract_text")
    def test_extract_text_with_easyocr(self, mock_easyocr, mock_preprocess):
        mock_easyocr.return_value = "Latte 3.00"
        mock_preprocess.return_value = "sample_preprocessed.png"
        result = utils.extract_text("sample.jpg", use_easyocr=True)
        self.assertIn("Latte", result)

    # Checks error returned when trying to generate AI JSON from poor input
    def test_generate_json_ai_with_poor_text(self):
        result = utils.generate_json_ai("hi")
        self.assertIn("error", result)

    # Simulates successful Gemini AI JSON generation
    @patch("api.ocrapp.utils.genai.GenerativeModel")
    @patch("api.ocrapp.utils.genai.configure")
    @patch("os.getenv", return_value="fake-key")
    def test_generate_json_ai_success(
        self, mock_getenv, mock_configure, mock_model_class
    ):
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"establishment": "Cafe", "total_price": "3.00"}'
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = utils.generate_json_ai("Latte 3.00\nTotal: 3.00")
        self.assertEqual(result["establishment"], "Cafe")

    # This simulates AI returning invalid JSON and checks error handling
    @patch("api.ocrapp.utils.genai.GenerativeModel")
    @patch("api.ocrapp.utils.genai.configure")
    @patch("os.getenv", return_value="fake-key")
    def test_generate_json_ai_invalid_json(
        self, mock_getenv, mock_configure, mock_model_class
    ):
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Invalid response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = utils.generate_json_ai("Latte 3.00\nTotal: 3.00")
        self.assertIn("error", result)


# Ensures the test file can run on its own
if __name__ == "__main__":
    unittest.main()


# Separate Django TestCase to test the /ocr-extract/ endpoint
from django.test import TestCase


class OCRExtractEndpointTest(TestCase):
    def test_no_file_uploaded_returns_error(self):
        """
        Ensure the /ocr-extract/ endpoint returns 400 if no file is uploaded.
        """
        response = self.client.post("/api/ocr-extract/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
