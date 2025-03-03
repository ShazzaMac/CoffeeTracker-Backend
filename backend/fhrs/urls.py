from django.urls import path
from .views import CoffeeShopListView

urlpatterns = [
path("shop-profile/", CoffeeShopListView.as_view(), name="shop-profile"),
path("api/cafes/", CoffeeShopListView.as_view(), name="api-cafes"),

]
