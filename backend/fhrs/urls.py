# ---------------------------------------------------------------
# Django URL configuration for the Coffee Shop app
#ref https://ratings.food.gov.uk/open-data-resources/documents/FHRS_APIv1_guidance_april24.pdf
# ---------------------------------------------------------------
from django.urls import path
from .views import CoffeeShopListView

urlpatterns = [
    path("shop-profile/", CoffeeShopListView.as_view(), name="shop-profile"),
    path("api/cafes/", CoffeeShopListView.as_view(), name="api-cafes"),
]
