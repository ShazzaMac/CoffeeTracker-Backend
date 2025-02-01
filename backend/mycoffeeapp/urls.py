from django.contrib import admin
from django.urls import (include,  # 'include' is important to link app URLs
                         path)
from registration.views import (ForgotPasswordView, LoginView,
                                ResetPasswordView, UserRegistrationView)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # Different method of authentication
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # --potentially redundant so have replaced this with the one below -- path('api/register/', include('registration.urls')),
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path("admin/", admin.site.urls),
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "api/reset-password/<uid>/<token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path("api/", include("fhrs.urls")),
]
