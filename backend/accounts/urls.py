# accounts/urls.py
from django.urls import path
from .views import ProfileUpdateView, PasswordChangeView

urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
]
