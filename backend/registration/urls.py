# this file is used to define the URL patterns for the registration app 
# which will be used to access the registration views. In simple terms, 
# this file is used to map URLs to views.
from django.urls import path
from registration.views import RegistrationView

urlpatterns = [
    # other URL patterns...
    path('accounts/register/', RegistrationView.as_view(), name='registration_register'),
]
