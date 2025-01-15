# this is the file where we define the utility functions that are in our application

from django.utils.crypto import get_random_string

def generate_secure_password():
    return get_random_string(length=12)  # Generates a 12-character random password
# Compare this snippet from backend/registration/views.py:
# # registration/views.py (for DRF API)
