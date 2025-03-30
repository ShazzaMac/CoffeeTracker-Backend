from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Views
from .views import (
    upload_file,
    save_extracted_data,
    results_data,
    results_page,
    get_csrf_token,
    csrf_token,
    contact_form,
    leaderboard_list,
    update_leaderboard,
    user_profile,
    my_view,  # Added my_view for testing
)

# FHRS + Registration
from fhrs.views import CoffeeShopListView
from registration.views import (
    ForgotPasswordView,
    LoginView,
    ResetPasswordView,
    UserRegistrationView,
)

# API Documentation (drf-spectacular)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# JWT Auth
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # JWT Auth Endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API Docs - may need to review
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    # User & Authentication urls
    path("api/user/", user_profile, name="user-profile"),
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("api/reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-password"),

    # Price form  & Tracker
    path("api/submit-price/", include("priceapp.urls")),
    path("api/prices/", include("priceapp.urls")),
    path("api/price/", include("priceapp.urls")),  # You might consolidate this later

    # OCR Logic for price form
    path("api/", include("api.ocrapp.urls")),

    # Contact form in about page
    path("api/contact/", contact_form, name="contact_form"),

    # Leaderboard
    path("api/leaderboard/", leaderboard_list, name="leaderboard-list"),
    path("api/update-leaderboard/", update_leaderboard, name="update-leaderboard"),

    # for CSRF Token to work, dont remove
    path("api/csrf/", get_csrf_token, name="get_csrf_token"),
    path("csrf-token/", csrf_token, name="csrf_token"),  # Leave as-is
    path("api/csrf-token/", csrf_token, name="csrf_token"),

    # File Upload + Results
    path("api/upload/", upload_file, name="upload"),
    path("api/save-extracted-data/", save_extracted_data, name="save_extracted_data"),
    path("api/results/", results_data, name="results"),
    path("results/", results_page, name="results_page"),

    # Coffee Shops (FHRS)
    path("fhrs/", include("fhrs.urls")),
    path("api/fhrs/", include("fhrs.urls")),
    path("api/cafes/", CoffeeShopListView.as_view(), name="api-cafes"),
    path("shop-profile/", CoffeeShopListView.as_view(), name="shop-profile"),

    # for the Accounts App
    path("accounts/", include("accounts.urls")),
    path("api/accounts/", include("accounts.urls")),

    # to access Django Admin
    path("admin/", admin.site.urls),

    # for testing purposes
       path("api/test-post/", my_view, name="my_view_test"),  
 
]

# Serves uploaded media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
