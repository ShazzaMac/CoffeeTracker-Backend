# ------------------------------------------
# this is an Asynchronous server gateway interface (ASGI) 
# configuration file for a Django project that is included in the backend directory.
# It sets up the ASGI application for the project, which is used to handle asynchronous requests.
# ------------------------------------------

"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mycoffeeapp.settings")

application = get_asgi_application()
