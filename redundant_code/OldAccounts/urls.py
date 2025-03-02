from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import UserProfileView, upload_profile_photo, ProfileUpdateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path ('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/' , UserProfileView.as_view(), name='user-profile'),
    path('upload-photo/', upload_profile_photo, name='upload-profile-photo'),
    path('api/accounts/profile/update', ProfileUpdateView.as_view(), name='profile-update'),
]


# Ensure media file handling is correct
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
