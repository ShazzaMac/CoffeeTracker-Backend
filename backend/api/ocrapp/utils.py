import pytesseract
import os
import json
import re
import cv2
import numpy as np
from PIL import Image
import subprocess
from pdf2image import convert_from_path
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Set the correct Tesseract path (for macOS)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# ✅ Load environment variables (for Gemini API)
load_dotenv()

# ✅ Allowed file types
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Convert HEIC to JPG
def convert_heic_to_jpg(img_path):
    new_path = img_path.rsplit(".", 1)[0] + ".jpg"
    try:
        subprocess.run(["sips", "-s", "format", "jpeg", img_path, "--out", new_path], check=True)
        return new_path
    except Exception as e:
        return None

# ✅ Extract text from images and PDFs
def extract_text(file_path):
    try:
        # ✅ Handle PDFs
        if file_path.lower().endswith(".pdf"):
            images = convert_from_path(file_path, dpi=400)
            if not images:
                return "Error: No images found in PDF."
            image = images[0]  # Use first page
        else:
            image = Image.open(file_path)

        # ✅ Convert image to grayscale
        image = image.convert("L")
        open_cv_image = np.array(image)

        # ✅ Apply Mild Denoising (Avoid Over-processing)
        denoised = cv2.fastNlMeansDenoising(open_cv_image, 1, 1, 1)

        # ✅ Apply Mild Sharpening Kernel (Avoid Extreme Enhancements)
        kernel = np.array([[0, -1, 0], [-1,  5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(denoised, -1, kernel)

        # ✅ Save processed image
        temp_path = file_path.rsplit(".", 1)[0] + "_sharpened.png"
        cv2.imwrite(temp_path, sharpened)

        # ✅ Perform OCR
        text = pytesseract.image_to_string(temp_path, lang="eng", config="--psm 6")

        return text
    except Exception as e:
        return f"Error processing file: {e}"

# ✅ Extract structured data from OCR text using Gemini AI
def generate_json_ai(text):
    try:
        if not text.strip() or len(text.split()) < 3:
            return {"error": "OCR output is too poor to process. Please try another image."}

        api_key = os.getenv("TOKEN_API_GEMINI")
        if not api_key:
            raise ValueError("API Key is missing. Set TOKEN_API_GEMINI in .env")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = (
            "Analyze the extracted receipt text and convert it into structured JSON:\n"
            "Fields needed: establishment name, date, beverage, and price.\n\n"
            f"Extracted text:\n{text}"
        )

        response = model.generate_content(prompt)
        clean_response = re.sub(r'```json|```', '', response.text).strip()
        return json.loads(clean_response)

    except Exception as e:
        return {"error": f"Failed to generate structured data: {e}"}
