import os
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.db import connection
from django.conf import settings
from .ocr_utils import extract_text, generate_json_ai, allowed_file
from django.views.decorators.csrf import csrf_exempt


# Ensure upload folder exists
UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def upload_file(request):
    """Handle image upload, extract text with OCR, and send extracted data + user inputs back to frontend."""
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        user_inputs = json.loads(request.POST.get('formData', '{}'))  # Get user inputs

        if allowed_file(file.name):
            file_path = default_storage.save(f"{settings.MEDIA_ROOT}/uploads/{file.name}", file)

            # Extract text with OCR
            text = extract_text(file_path)

            # Process text with Gemini AI
            extracted_data = generate_json_ai(text)

            # Send extracted data + user inputs to frontend
            return JsonResponse({
                "extracted_data": extracted_data,
                "user_inputs": user_inputs,
            })

    return JsonResponse({'error': 'Invalid file type or missing file'}, status=400)

@csrf_exempt
def save_extracted_data(request):
    """Save extracted OCR data + user inputs to the database."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            extracted_data = data.get("extractedData", [])
            user_inputs = data.get("userInputs", {})

            final_data = {
                "extracted_data": extracted_data,
                "user_inputs": user_inputs,
            }

            # Store in PostgreSQL
            with connection.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS shop_res (
                        id SERIAL PRIMARY KEY,
                        json_data TEXT NOT NULL
                    )
                ''')
                cursor.execute("INSERT INTO shop_res (json_data) VALUES (%s)", [json.dumps(final_data)])

            return JsonResponse({"message": "Data saved successfully!"}, status=201)

        except Exception as e:
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
    return JsonResponse({'results': results})


from django.shortcuts import render

def index(request):
    return render(request, 'mycoffeeapp/base.html')  # Render the base.html template
