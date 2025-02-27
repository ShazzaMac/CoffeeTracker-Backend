# backend/accounts/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Endpoint to obtain access & refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint to refresh the access token using the refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/upload-photo/', views.upload_photo, name='upload_photo'),
    
]
