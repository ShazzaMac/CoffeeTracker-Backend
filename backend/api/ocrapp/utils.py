import pytesseract
import os
import json
import re
import cv2
import numpy as np
from PIL import Image
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai
import easyocr

# ✅ Load environment variables (for Gemini API)
load_dotenv()

# ✅ Set the correct Tesseract path (for macOS)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

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

# ✅ Extract text using EasyOCR
def easyocr_extract_text(image_path):
    """Extracts text using EasyOCR."""
    reader = easyocr.Reader(["en"])
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)

# ✅ Preprocess Image for Better OCR
def preprocess_image(image_path):
    """Apply light preprocessing (avoid over-processing)."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 🔹 Lightly sharpen instead of thresholding
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    processed = cv2.filter2D(image, -1, kernel)

    # Save processed image
    temp_path = image_path.rsplit(".", 1)[0] + "_preprocessed.png"
    cv2.imwrite(temp_path, processed)

    if not os.path.exists(temp_path):
        print(f"❌ ERROR: Processed image did not save at {temp_path}")
    else:
        print(f"✅ Processed Image Saved: {temp_path}")

    return temp_path

# ✅ Extract text from images and PDFs
def extract_text(file_path, use_easyocr=False):
    try:
        # ✅ Handle PDFs
        if file_path.lower().endswith(".pdf"):
            images = convert_from_path(file_path, dpi=300)
            if not images:
                return "Error: No images found in PDF."
            image = images[0]  # Use first page
            image.save(file_path.replace(".pdf", ".jpg"))  # Convert for OCR
            file_path = file_path.replace(".pdf", ".jpg")

        # ✅ Preprocess Image
        processed_image_path = preprocess_image(file_path)

        # ✅ Perform OCR with EasyOCR or Tesseract
        if use_easyocr:
            extracted_text = easyocr_extract_text(processed_image_path)
        else:
            extracted_text = pytesseract.image_to_string(Image.open(processed_image_path), lang="eng", config="--psm 4")

        # 🔹 Debugging Log
        print(f"🔎 Extracted Text:\n{extracted_text}")

        # ✅ Return text
        return extracted_text if extracted_text.strip() else "Error: No text found in OCR."

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
            "Analyze the extracted receipt text and convert it into structured JSON.\n"
            "Provide valid JSON output containing:\n"
            "- `establishment`: Name of the establishment\n"
            "- `date`: Date of the receipt\n"
            "- `items`: List of beverages and their prices\n"
            "- `total_price`: Total amount paid\n\n"
            f"Extracted text:\n{text}"
        )

        response = model.generate_content(prompt)

        # ✅ Ensure AI response is not empty
        if not response.text.strip():
            return {"error": "Gemini AI returned an empty response."}

        # ✅ Ensure AI response is valid JSON
        try:
            clean_response = re.sub(r'```json|```', '', response.text).strip()
            structured_data = json.loads(clean_response)
            return structured_data  # ✅ Return valid JSON
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse AI response: {e}", "raw_response": response.text}

    except Exception as e:
        return {"error": f"Failed to generate structured data: {e}"}
