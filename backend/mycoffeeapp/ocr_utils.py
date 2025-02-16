# mycoffeeapp/ocr_utils.py
import os
import json
import re
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import google.generativeai as genai
from django.conf import settings

# Load environment variables
load_dotenv()

# Ensure Tesseract path is set (only needed for Windows, remove for Mac/Linux)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if file is an allowed image type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(img_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(img_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error processing image: {e}"

def generate_json_ai(text):
    """Process extracted text with Gemini AI to structure it into JSON format."""
    try:
        genai.configure(api_key=os.getenv("TOKEN_API_GEMINI"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Please analyze the menu photo and extract information for each product. "
            "For each product, provide details in JSON format: "
            "- Product title "
            "- Product description "
            "- Product price "
            "Each product should be structured as an object with `title`, `description`, and `price`. "
            "Here is the extracted menu text:\n\n"
            f"{text}"
        )

        response = model.generate_content(prompt)
        clean_response = re.sub(r'```json|```', '', response.text).strip()
        return json.loads(clean_response)
    except Exception as e:
        return {"error": f"Failed to generate JSON: {e}"}
