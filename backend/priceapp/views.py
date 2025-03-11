import json
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PriceSubmission
from .serializers import PriceSubmissionSerializer
from rest_framework.generics import ListAPIView

# +-----------------------------------------------------+

class PriceListView(ListAPIView):
    queryset = PriceSubmission.objects.all()
    serializer_class = PriceSubmissionSerializer


class PriceSubmissionListView(generics.ListAPIView):
    queryset = PriceSubmission.objects.all()
    serializer_class = PriceSubmissionSerializer


def str_to_bool(value):
    """Convert 'true'/'false' strings to boolean values."""
    if isinstance(value, bool):  # Already a boolean
        return value
    return value.lower() == "true"

class PriceSubmissionView(APIView):
    def post(self, request):
        """Handle new price submissions"""
        file = request.FILES.get("file", None)

        if request.content_type == "application/json":
            form_data = request.data  # JSON is already parsed
        else:
            form_data_str = request.POST.get("formData", None)
            if not form_data_str:
                return Response({"error": "formData is missing"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                form_data = json.loads(form_data_str)
            except json.JSONDecodeError:
                return Response({"error": "Invalid form data JSON"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert string booleans to actual booleans
        features = form_data["features"]
        ratings = form_data["ratings"]

        submission = PriceSubmission.objects.create(
            establishment=form_data["establishment"],
            date=form_data["date"],
            beverage=form_data["beverage"],
            price=form_data["price"],
            submitter_name=form_data["submitterName"],
            dog_friendly=str_to_bool(features["dogFriendly"]),
            wifi=str_to_bool(features["wifi"]),
            outdoor_seating=str_to_bool(features["outdoorSeating"]),
            plant_milks=str_to_bool(features["plantMilks"]),
            brunch_lunch=str_to_bool(features["brunchLunch"]),
            wheelchair_access=str_to_bool(features["wheelchairAccess"]),
            coffee_taste=ratings["coffeeTaste"],
            coffee_options=ratings["coffeeOptions"],
            service=ratings["service"],
            atmosphere=ratings["atmosphere"],
            value_for_money=ratings["valueForMoney"],
            receipt=file if file else None,
        )

        return Response(PriceSubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """Retrieve all submissions"""
        submissions = PriceSubmission.objects.all()
        serializer = PriceSubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
