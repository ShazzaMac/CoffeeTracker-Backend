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
from rest_framework.views import APIView
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.ocrapp.utils import extract_text, generate_json_ai
from .models import ShopResult, ContactMessage
from .models import ContactMessage
logger = logging.getLogger(__name__)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Leaderboard
from .serializers import LeaderboardSerializer

@api_view(['GET'])
def leaderboard_list(request):
    """Fetches the top 10 players sorted by highest score."""
    top_players = Leaderboard.objects.order_by('-points')[:10]
    serializer = LeaderboardSerializer(top_players, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])  # for authentication use IsAuthenticated
def update_leaderboard(request):
    """Updates the leaderboard with the authenticated user's score."""
    user = request.user
    points = request.data.get('points')

    if points is None:
        return Response({"error": "Points are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Either create a new entry or update existing one (keeping highest score)
    leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user, defaults={'points': points})

    if not created and points > leaderboard_entry.points:
        leaderboard_entry.points = points
        leaderboard_entry.save()

    return Response(LeaderboardSerializer(leaderboard_entry).data, status=status.HTTP_201_CREATED)


def csrf_token(request):
    return JsonResponse({'csrf_token': get_token(request)})



def contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            # Log the parsed JSON data
            logger.info("Parsed JSON data: %s", data)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")
        
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Log each field's value and type
        logger.info("Name: %r (%s)", name, type(name))
        logger.info("Email: %r (%s)", email, type(email))
        logger.info("Message: %r (%s)", message, type(message))

        if not name or not email or not message:
            return HttpResponseBadRequest("All fields are required.")
        
        # Save the contact message to the database
        contact_message = ContactMessage.objects.create(name=name, email=email, message=message)

        return JsonResponse({"success": "Message sent successfully!"}, status=201)
    
    return HttpResponseBadRequest("Invalid method.")

# +-----------------------------------------------------+

# Ensure upload folder exists
UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

def get_csrf_token(request):
    """Get CSRF token for frontend."""
    if request.method == "GET":
        token = get_token(request)
        return JsonResponse({"csrfToken": token})
    return JsonResponse({"error": "Invalid request"}, status=400)

def allowed_file(filename):
    """Check if the file type is allowed."""
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

            final_data = {
                "extracted_data": extracted_data,
                "user_inputs": user_inputs,
            }

            shop_result = ShopResult.objects.create(json_data=json.dumps(final_data))

            return JsonResponse({"message": "Data saved successfully!", "id": shop_result.id}, status=201)

        except Exception as e:
            logger.error(f"Error saving data: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

def results_page(request):
    """Render results page."""
    return render(request, "results.html")

def results_data(request):
    """Fetch results from database."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT json_data FROM shop_res")
        results = [row[0] for row in cursor.fetchall()]
    return JsonResponse({"results": results})

def index(request):
    """Render the base.html template."""
    return render(request, "mycoffeeapp/base.html")

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
