# ----------------------------------------------------------------
# These urls are for the OCR app, which handles image processing and text extraction.
# ----------------------------------------------------------------

from django.urls import path
from .views import ocr_extract

urlpatterns = [
    path("ocr-extract/", ocr_extract, name="ocr-extract"),
]
