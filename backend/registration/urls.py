# this file is used to define the URL patterns for the registration app 
# which will be used to access the registration views. In simple terms, 
# this file is used to map URLs to views.
from django.urls import path
from .views import UserRegistrationView, LoginView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
]
