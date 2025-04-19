# +-----------------------------------------------------+
# this is the file contains reusable utility functions for the Django app.
# +-----------------------------------------------------+

from django.utils.crypto import get_random_string

def generate_secure_password():
    return get_random_string(length=12)  # Generates a 12-character random password

# +-----------------------------------------------------+

def allowed_file(filename):
    """Check if the file type is allowed."""
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# +-----------------------------------------------------+
