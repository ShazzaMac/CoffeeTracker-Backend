import os
import sys
from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-yh_k+-$rq=b$#096nu(4p%ycdkwh8zpv_y6*peca_+b7y23fj+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# This is the list of allowed hosts that can access the project
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# This is the list of installed apps that are required for the project to work
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "corsheaders",
    "registration",
    "fhrs",
    "rest_framework",
    "rest_framework_simplejwt",
    "priceapp",
    "api.ocrapp",
    "mycoffeeapp",
    "drf_spectacular",
    "accounts.apps.AccountsConfig",
    "django_otp",
    "django_otp.plugins.otp_totp",
]

# Static files (CSS, JavaScript, Images) which are required for the project to work
# These setting are for the django admin panel
SITE_ID = 1  # Required for Django sites framework
SESSION_ENGINE = "django.contrib.sessions.backends.db"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",  # Adjust if your static files are in a different directory
]


# this is for the registration app to work
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# middleware is a framework of hooks into Django's request/response processing
# It's a light, low-level plugin system for globally altering Django's input or output
# MIDDLEWARE is a list of middleware classes that have access to the request and response in Django
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # This middleware is required for security
    "django.contrib.sessions.middleware.SessionMiddleware",  # This middleware is required for Django sessions
    "django.middleware.common.CommonMiddleware",  # This middleware is required for CSRF protection
    "corsheaders.middleware.CorsMiddleware",  # This middleware is required for CORS which allows cross-origin requests
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # This middleware is required for Django authentication
    "django.contrib.messages.middleware.MessageMiddleware",  # This middleware is required for Django messages framework
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # This middleware is required for Clickjacking protection
    "django_ratelimit.middleware.RatelimitMiddleware",  # Rate limiting middleware
]


# CORS configuration is required to allow cross-origin requests
CORS_ALLOW_CREDENTIALS = True  # This allows cookies to be sent
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
]


# CSRF settings which are required for security
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",  # Backend
    "http://localhost:3000",  # React Frontend
    "http://127.0.0.1:8000/api/upload/",  # Upload endpoint
]
CSRF_COOKIE_SAMESITE = "None"  # For cross-site cookies
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read the CSRF cookie
CSRF_USE_SESSIONS = False
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_HTTPONLY = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False  # Set to True in production


# JWT settings which are required for authentication also and work  with csrf settings to ensure security
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # 5 minutes for access token
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 1 day for refresh token
    "ROTATE_REFRESH_TOKENS": True,  # To rotate the refresh token when it's used
    "BLACKLIST_AFTER_ROTATION": True,  # To blacklist old refresh tokens
}

# this is the list of the root urls that are required for the project to work
ROOT_URLCONF = "mycoffeeapp.urls"

# This is the list of the templates that are required for the project to work
# A template is a text file defining the structure or layout of a file (such as an HTML page), with placeholders used to represent actual data provided by a database or other source.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI is a specification that describes how a web server communicates with web applications
WSGI_APPLICATION = "mycoffeeapp.wsgi.application"

# Database configuration for my PostgreSQL database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "CoffeeApp",
        "USER": "postgres",
        "PASSWORD": "Plu13064005!",
        "HOST": "localhost",
        "PORT": "5433",
    }
}

# Password validation for user authentication
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization settings for the project
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# this means that the static files are stored in the static folder in the root directory
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging configuration for the project to log errors and warnings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",  # Change to "INFO" to see all logs
            "propagate": True,
        },
        "registration": {
            "handlers": ["console"],
            "level": "ERROR",
        },
    },
}

# Gmail settings for password reset emails
EMAIL_BACKEND_GMAIL = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_GMAIL = "smtp.gmail.com"
EMAIL_PORT_GMAIL = 587
EMAIL_USE_TLS_GMAIL = True
EMAIL_HOST_USER_GMAIL = "coffeetrackerapphelp@gmail.com"
EMAIL_HOST_PASSWORD_GMAIL = "pngo xmrk xpri yovw"
DEFAULT_FROM_EMAIL_GMAIL = "coffeetrackerapphelp@gmail.com"

# Outlook settings for contact form emails
EMAIL_BACKEND_OUTLOOK = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_OUTLOOK = "outlook.office365.com"
EMAIL_PORT_OUTLOOK = 587
EMAIL_USE_TLS_OUTLOOK = True
EMAIL_HOST_USER_OUTLOOK = "sharonplumridge@outlook.com"
EMAIL_HOST_PASSWORD_OUTLOOK = "Plu13064005"
DEFAULT_FROM_EMAIL_OUTLOOK = "sharonplumridge@outlook.com"


# Media files which are for user-uploaded files
MEDIA_ROOT = (
    BASE_DIR / "media"
)  # This is the directory where user-uploaded files are stored
MEDIA_URL = "/media/"

# Rate limiting which is required for security
RATELIMIT_VIEW = "django_ratelimit.views.ratelimited"
