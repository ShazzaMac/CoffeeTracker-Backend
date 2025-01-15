from django.contrib import admin
from django.urls import path, include  # 'include' is important to link app URLs
from django.urls import path
from registration.views import UserRegistrationView, LoginView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
]



