from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import (DashboardView, ForgotPasswordView, LoginView,
                    ProtectedEndpoint, ResetPasswordView, UserRegistrationView)

urlpatterns = [
    # Dashboard and protected endpoint
    path("api/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("api/protected-endpoint/", ProtectedEndpoint.as_view(), name="protected-endpoint"),

    # Token Authentication and JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # User Registration and Authentication
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("api/reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
]
