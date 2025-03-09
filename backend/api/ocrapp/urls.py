from django.urls import path
from .views import ocr_extract

urlpatterns = [
    path('ocr-extract/', ocr_extract, name='ocr-extract'),
]
