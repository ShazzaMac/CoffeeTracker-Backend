# this file is used to configure the app by defining the app configuration class.
# This class is used to define metadata for the app such as the app name and other configurations.
from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.registration"
