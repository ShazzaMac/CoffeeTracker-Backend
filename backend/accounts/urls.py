# backend/accounts/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Endpoint to obtain access & refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint to refresh the access token using the refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.get_user_profile, name='get_user_profile'),  # GET for profile data
    path('profile/update/', views.update_user_profile, name='update_user_profile'),  # POST for updating profile
]
