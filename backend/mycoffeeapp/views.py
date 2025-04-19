import os
import json
import logging
import smtplib

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from django.db import connection
from django.conf import settings
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from api.ocrapp.utils import extract_text, generate_json_ai
from .models import ShopResult, ContactMessage
from .models import ContactMessage
from .models import Leaderboard

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import LeaderboardSerializer


logger = logging.getLogger(__name__)

# +-----------------------------------------------------+
#                    LEADERBOARD VIEWS
# +-----------------------------------------------------+

@api_view(["GET"])
def leaderboard_list(request):
    """Fetches the top 10 players sorted by highest score."""
    top_players = Leaderboard.objects.order_by("-points", "timestamp")[:10]
    serializer = LeaderboardSerializer(top_players, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_leaderboard(request):
    """Save a new leaderboard entry each time a user submits a score."""
    user = request.user
    points = request.data.get("points")

    if points is None:
        return Response(
            {"error": "Points are required"}, status=status.HTTP_400_BAD_REQUEST
        )
    new_entry = Leaderboard.objects.create(user=user, points=points)

    # Returns the full leaderboard sorted by highest score
    top_players = Leaderboard.objects.order_by("-points")[:10]
    return Response(
        LeaderboardSerializer(top_players, many=True).data,
        status=status.HTTP_201_CREATED,
    )

# +-----------------------------------------------------+
#                    CSRF TOKEN VIEWS
# +-----------------------------------------------------+

# upddated
@api_view(["GET"])
def csrf_token(request):
    """Return CSRF token explicitly allowing CORS (for frontend access)."""
    response = JsonResponse({"csrf_token": get_token(request)})
    response["Access-Control-Allow-Origin"] = (
        "*"  # Remove in production; set allowed domains instead
    )
    response["Access-Control-Allow-Methods"] = "GET"
    return response

def get_csrf_token(request):
    """Get CSRF token for frontend."""
    if request.method == "GET":
        token = get_token(request)
        return JsonResponse({"csrfToken": token})
    return JsonResponse({"error": "Invalid request"}, status=400)

# +-----------------------------------------------------+
#                    CONTACT FORM VIEWS
# +-----------------------------------------------------+

def contact_form(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            # Log the parsed JSON data
            logger.info("Parsed JSON data: %s", data)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        # Log each field's value and type
        logger.info("Name: %r (%s)", name, type(name))
        logger.info("Email: %r (%s)", email, type(email))
        logger.info("Message: %r (%s)", message, type(message))

        if not name or not email or not message:
            return HttpResponseBadRequest("All fields are required.")

        # updated -- sends to db
        ContactMessage.objects.create(name=name, email=email, message=message)
        return JsonResponse({"success": "Message sent successfully!"}, status=201)

    return HttpResponseBadRequest("Invalid method.")


# +-----------------------------------------------------+
#                    UPLOAD VIEWS
# +-----------------------------------------------------+

# Ensures upload folder exists
UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if the file type is allowed."""
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(request):
    """Handle file upload, extract text, and process with AI."""
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        if not allowed_file(file.name):
            return JsonResponse({"error": "Invalid file type"}, status=400)

        file_path = default_storage.save(f"uploads/{file.name}", file)

        # Extract text with OCR
        text = extract_text(file_path)

        # Process text with Gemini AI
        extracted_data = generate_json_ai(text)

        return JsonResponse({"extracted_data": extracted_data})

    return JsonResponse({"error": "Invalid request"}, status=400)


def save_extracted_data(request):
    """Save extracted OCR data + user inputs to the database."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            extracted_data = data.get("extractedData", [])
            user_inputs = data.get("userInputs", {})

            if not extracted_data:
                return JsonResponse({"error": "No extracted data found"}, status=400)

            final_data = {
                "extracted_data": extracted_data,
                "user_inputs": user_inputs,
            }

            shop_result = ShopResult.objects.create(json_data=json.dumps(final_data))

            return JsonResponse(
                {"message": "Data saved successfully!", "id": shop_result.id},
                status=201,
            )

        except Exception as e:
            logger.error(f"Error saving data: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# +-----------------------------------------------------+
#                    RESULTS VIEWS
# +-----------------------------------------------------+

def results_page(request):
    """Render results page."""
    return render(request, "results.html")

def index(request):
    """Render the base.html template."""
    return render(request, "mycoffeeapp/base.html")


# +-----------------------------------------------------+
#                    DATABASE VIEWS
# +-----------------------------------------------------+
def results_data(request):
    """Fetch results from database."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT json_data FROM shop_res")
        results = [row[0] for row in cursor.fetchall()]
    return JsonResponse({"results": results})

# +-----------------------------------------------------+
#                    CSRF TOKEN DEBUGGING
# +-----------------------------------------------------+


def your_view(request):
    """Debug CSRF token issues."""
    csrf_token_cookie = request.COOKIES.get("csrftoken")
    csrf_token_meta = request.META.get("HTTP_X_CSRFTOKEN")  # Check request headers

    if not csrf_token_cookie:
        logger.warning("No CSRF token found in cookies.")

    if csrf_token_meta != csrf_token_cookie:
        logger.error("CSRF token mismatch: request does not match cookie.")

    return JsonResponse({"message": "Success"})


# +-----------------------------------------------------+
# |   # REMOVE this in production (only for testing)    |
# +-----------------------------------------------------+

def my_view(request):
    if request.method == "POST":
        return JsonResponse({"message": "POST request successful"})
    return JsonResponse({"error": "Invalid request"}, status=400)


# +-----------------------------------------------------+
#                    USER PROFILE VIEW
# +-----------------------------------------------------+


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Returns the authenticated user's details."""
    user = request.user
    return Response({"username": user.username, "email": user.email})

class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
