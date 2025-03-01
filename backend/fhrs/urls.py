from django.urls import path
from .views import CoffeeShopListView

urlpatterns = [
path("shop-profile/", CoffeeShopListView.as_view(), name="shop-profile"),

]
