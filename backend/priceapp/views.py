from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PriceSubmission
from .serializers import PriceSubmissionSerializer

class PriceSubmissionView(APIView):
    def post(self, request):
        """Handle new price submissions"""
        file = request.FILES.get("file", None)
        form_data = request.data.get("formData")

        # Convert JSON string to dict (because formData is sent as JSON string)
        import json
        try:
            form_data = json.loads(form_data)
        except json.JSONDecodeError:
            return Response({"error": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new submission
        submission = PriceSubmission.objects.create(
            establishment=form_data["establishment"],
            date=form_data["date"],
            beverage=form_data["beverage"],
            price=form_data["price"],
            submitter_name=form_data["submitterName"],
            dog_friendly=form_data["features"]["dogFriendly"],
            wifi=form_data["features"]["wifi"],
            outdoor_seating=form_data["features"]["outdoorSeating"],
            plant_milks=form_data["features"]["plantMilks"],
            brunch_lunch=form_data["features"]["brunchLunch"],
            wheelchair_access=form_data["features"]["wheelchairAccess"],
            coffee_taste=form_data["ratings"]["coffeeTaste"],
            coffee_options=form_data["ratings"]["coffeeOptions"],
            service=form_data["ratings"]["service"],
            atmosphere=form_data["ratings"]["atmosphere"],
            value_for_money=form_data["ratings"]["valueForMoney"],
            receipt=file if file else None,
        )

        return Response(PriceSubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """Retrieve all submissions"""
        submissions = PriceSubmission.objects.all()
        serializer = PriceSubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
