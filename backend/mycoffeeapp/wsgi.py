#   ---------------------------------------------------------------------
# This is a Web Server Gateway Interface (WSGI) configuration file for a Django project.
# It sets up the WSGI application for the project, which is used to serve the application
# through a WSGI server. The WSGI application is the entry point for the web server to communicate with the Django application.
# ---------------------------------------------------------------------

"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mycoffeeapp.settings")

application = get_wsgi_application()
