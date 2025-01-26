from django.urls import path
from .views import CoffeeShopListView

urlpatterns = [
    path("cafes/", CoffeeShopListView.as_view(), name="cafe-list"),
]
