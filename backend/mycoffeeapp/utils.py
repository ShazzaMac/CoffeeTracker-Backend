# this is the file where we define the utility functions that are in our application

from django.utils.crypto import get_random_string


def generate_secure_password():
    return get_random_string(length=12)  # Generates a 12-character random password


# Compare this snippet from backend/registration/views.py:
# # registration/views.py (for DRF API)


# from django.contrib.auth.models import extracted data
from django.urls import path
from .views import upload_file, save_extracted_data

urlpatterns = [
    path('upload/', upload_file),
    path('save-extracted-data/', save_extracted_data),
]
