from django.contrib import admin
from django.urls import include, path
from backend.registration_api.views import ForgotPasswordView, LoginView, ResetPasswordView, UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path("admin/", admin.site.urls),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("api/reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
    path("api/", include("backend.fhrs_api.urls")),
    path("api/", include("backend.registration_api.urls")),
    path("api/contact/", include("backend.contact_api.urls")),
]

