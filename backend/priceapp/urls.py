# --------------------------------------------------------------------------------
# urls for the priceapp
# --------------------------------------------------------------------------------
from django.urls import path
from .views import PriceSubmissionView
from priceapp.views import PriceListView


urlpatterns = [
    path(
        "", PriceSubmissionView.as_view(), name="submit-price"
    ), 
    path("api/prices/", PriceListView.as_view(), name="price-list"),
]
