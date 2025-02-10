# fhrs_api/urls.py
from django.urls import path
from . import views
from .views import CoffeeShopListView

urlpatterns = [
    path("cafes/", CoffeeShopListView.as_view(), name="cafe-list"),
]
