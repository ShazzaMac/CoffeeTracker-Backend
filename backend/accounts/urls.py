# backend/accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.get_user_profile, name='get_user_profile'),  # GET for profile data
    path('profile/update/', views.update_user_profile, name='update_user_profile'),  # POST for updating profile
]
