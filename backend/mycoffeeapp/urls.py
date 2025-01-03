# mycoffeeapp/urls.py
from django.contrib import admin
from django.urls import path, include
from registration.views import UserRegistrationView  # Import the relevant view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('register/', UserRegistrationView.as_view(), name='register'),  # Registration view
    # You can add other paths here as needed
]
