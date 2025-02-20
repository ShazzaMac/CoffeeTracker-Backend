from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from .views import upload_file, save_extracted_data, results_data, results_page
from django.conf import settings
from django.conf.urls.static import static
from .views import get_csrf_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



from registration.views import (
    ForgotPasswordView,
    LoginView,
    ResetPasswordView,
    UserRegistrationView,
)
from rest_framework_simplejwt import views as jwt_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path("admin/", admin.site.urls),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("api/reset-password/<uid>/<token>/",ResetPasswordView.as_view(), name="reset-password"),
    path("api/", include("fhrs.urls")),
    path('api/upload/', upload_file, name='upload'),  
    path('api/save-extracted-data/', save_extracted_data, name='save_extracted_data'),
    path('api/results/', results_data, name='results'),
    path('results/', results_page, name='results_page'),
    path('accounts/', include('accounts.urls')),
    path('api/accounts/', include('accounts.urls')),  
    path("api/", include("priceapp.urls")), 
    path("api/csrf/", get_csrf_token, name="get_csrf_token"), 

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 
