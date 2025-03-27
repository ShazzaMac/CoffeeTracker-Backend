import json
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PriceSubmission
from .serializers import PriceSubmissionSerializer
from django.core.exceptions import ValidationError

# Helper function
def str_to_bool(value):
    """Convert 'true'/'false' strings to boolean values."""
    if isinstance(value, bool):
        return value
    return value.lower() == "true"

# GET all submissions
class PriceListView(generics.ListAPIView):
    queryset = PriceSubmission.objects.all()
    serializer_class = PriceSubmissionSerializer

# POST new submission + GET all (duplicate route fallback)
class PriceSubmissionView(APIView):
    def post(self, request):
        """Handle new price submissions"""
        file = request.FILES.get("file", None)

        if request.content_type == "application/json":
            form_data = request.data  # Already parsed
        else:
            form_data_str = request.POST.get("formData", None)
            if not form_data_str:
                return Response({"error": "formData is missing"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                form_data = json.loads(form_data_str)
            except json.JSONDecodeError:
                return Response({"error": "Invalid form data JSON"}, status=status.HTTP_400_BAD_REQUEST)

        try:
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

        except (KeyError, ValueError, TypeError, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Retrieve all submissions"""
        submissions = PriceSubmission.objects.all()
        serializer = PriceSubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
