from django.apps import AppConfig
from django_ratelimit.decorators import ratelimit


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.api"  # Updated to match its location.
