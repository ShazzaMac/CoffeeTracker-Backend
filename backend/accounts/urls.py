# ----------------------------------------------------------------
# These urls are for the accounts app, which handles user profiles and password changes.
# ----------------------------------------------------------------
from django.urls import path
from .views import ProfileUpdateView, PasswordChangeView

urlpatterns = [
    path("profile/", ProfileUpdateView.as_view(), name="profile-update"),
    path("change-password/", PasswordChangeView.as_view(), name="change-password"),
]
