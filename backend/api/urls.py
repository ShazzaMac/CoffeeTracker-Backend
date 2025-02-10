from django.urls import path
from . import views

urlpatterns = [
    path('', views.api, name='api'),
    path('api/contact/', views.contact_form, name='contact_form'),
]
