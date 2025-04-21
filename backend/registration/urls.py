# --------------------------------------------------------------------------------
# this file is used to define the URL patterns for the registration app
# which will be used to access the registration views.
# --------------------------------------------------------------------------------
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PriceSubmissionListView
from . import views
from .views import (
    DashboardView,
    ForgotPasswordView,
    LoginView,
    ProtectedEndpoint,
    ResetPasswordView,
    UserRegistrationView,
)

urlpatterns = [
    path("api/dashboard/", DashboardView.as_view(), name="dashboard"),
    path(
        "api/protected-endpoint/",
        ProtectedEndpoint.as_view(),
        name="protected-endpoint",
    ),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # trying JWT (JSON Web Tokens) Authentication
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-token-auth/", obtain_auth_token, name="login"),
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "api/reset-password/<uid>/<token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
