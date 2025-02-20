from django.urls import path
from .views import PriceSubmissionView

urlpatterns = [
    path("upload/", PriceSubmissionView.as_view(), name="price-upload"),
]
