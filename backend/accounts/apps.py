# ------------------------------------------------------------
# This file is used to configure the accounts application.
# It sets the default auto field type and ensures that signals are loaded when the app is ready.
# ------------------------------------------------------------
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals  # Ensure the signal is loaded
