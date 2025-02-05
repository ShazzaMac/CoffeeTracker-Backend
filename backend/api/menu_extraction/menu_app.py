import os
import json
import re
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import google.generativeai as genai
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import connection

# Load environment variables
load_dotenv()

# Ensure Tesseract path is set
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Ensure upload folder exists
UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, 'api/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text from image using Tesseract
def extract_text(img_path):
    try:
        image = Image.open(img_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error processing image: {e}"

# Generate JSON data from extracted text using Gemini AI
def generate_json_ai(text):
    try:
        genai.configure(api_key=os.getenv("TOKEN_API_GEMINI"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Please analyse the menu photo and extract information for each product. "
            "For each product, provide the following details in JSON format: "
            "- Product title "
            "- Product description "
            "- Product price "
            "Each product should be represented as an object with the keys `title`, `description`, and `price`. "
            "The final result should be a list of JSON objects, where each object represents a menu item. "
            "Example format: "
            "[ "
            "{ \"title\": \"Product 1\", \"description\": \"Description of Product 1\", \"price\": \"£10.00\" }, "
            "{ \"title\": \"Product 2\", \"description\": \"Description of Product 2\", \"price\": \"£20.00\" }, "
            "{ \"title\": \"Product 3\", \"description\": \"Description of Product 3\", \"price\": \"£30.00\" } "
            "] "
            f"Ensure that the description and price are clearly identified and that the price format is consistent (e.g., £10.00 or 10.00). Here is the menu: {text}"
        )

        response = model.generate_content(prompt)
        clean_response = re.sub(r'```json|```', '', response.text).strip()
        data = json.loads(clean_response)
        return data
    except Exception as e:
        return {"error": f"Failed to generate JSON: {e}"}

# Handle image upload and processing
def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        
        if allowed_file(file.name):
            file_path = os.path.join(UPLOAD_FOLDER, file.name)
            path = default_storage.save(file_path, file)

            text = extract_text(path)
            result = generate_json_ai(text)
            result_json = json.dumps(result)

            with connection.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS shop_res (
                    id SERIAL PRIMARY KEY,
                    json_data TEXT NOT NULL
                    )
                ''')
                cursor.execute("INSERT INTO shop_res (json_data) VALUES (%s)", [result_json])
            
            return redirect('results_page')
        return JsonResponse({'error': 'Invalid file type'}, status=400)
    return JsonResponse({'error': 'No file uploaded'}, status=400)

# Display results page
def results_page(request):
    return render(request, "results.html")

# Fetch results data from the database
def results_data(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT json_data FROM shop_res")
        results = [row[0] for row in cursor.fetchall()]
    return JsonResponse({'results': results})

# Delete all stored menu data
def delete_all(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM shop_res")
        return redirect('index')
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Main index route
def index(request):
    return render(request, "index.html")
