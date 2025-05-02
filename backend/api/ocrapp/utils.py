# ----------------------------------------------------------------
# This file contains utility functions for OCR processing.
# It includes functions for allowed file types, converting HEIC to JPG,
# extracting text from images and PDFs, preprocessing images, and generating structured JSON data using Gemini AI and
# Tesseract OCR.(other methods were attempted but not used in the end)
# This file includes helper functions for validating file types,
# converting HEIC images to JPG, extracting text from images and PDFs using Tesseract and EasyOCR,
# preprocessing images for better OCR results, and generating structured JSON data using Gemini AI.
# It also includes error handling and logging for debugging purposes.
 #resources: https://github.com/theiguim/gen_menu_ai, https://www.freecodecamp.org/news/getting-started-with-tesseract-part-ii-f7f9a0899b3f/
# https://stackoverflow.com/questions/32642421/opencv-altering-the-filter2d-function?rq=3
#https://www.freecodecamp.org/news/getting-started-with-tesseract-part-ii-f7f9a0899b3f/
# ----------------------------------------------------------------

import pytesseract
import os
import json
import re
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai
import easyocr


# Loads environment variables (for Gemini API to work)
load_dotenv()

# Sets the correct Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"


# Allowed file types:
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "heic", "heif", "pdf"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


#  Convert HEIC to JPG if uploading images from an apple device
def convert_heic_to_jpg(img_path):
    new_path = img_path.rsplit(".", 1)[0] + ".jpg"
    try:
        subprocess.run(
            ["sips", "-s", "format", "jpeg", img_path, "--out", new_path], check=True 
        )
        return new_path
    except Exception as e:
        return None


#  Extract text using EasyOCR - second option as fallback
def easyocr_extract_text(image_path):
    """Extracts text using EasyOCR."""
    reader = easyocr.Reader(["en"])
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)


# Preproceses Image for Better OCR to fix text extraction issues
def preprocess_image(image_path):
    """Apply light preprocessing (avoid over-processing)."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Lightly sharpens instead of thresholding - this has been manually adjusted to test results
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    processed = cv2.filter2D(image, -1, kernel) # code from - https://stackoverflow.com/questions/32642421/opencv-altering-the-filter2d-function?rq=3

    # Save processed image
    temp_path = image_path.rsplit(".", 1)[0] + "_preprocessed.png"
    cv2.imwrite(temp_path, processed)

    if not os.path.exists(temp_path):
        print(f" ERROR: Processed image did not save at {temp_path}")
    else:
        print(f" Processed Image Saved: {temp_path}")

    return temp_path


# Extracts text from images and PDFs
def extract_text(file_path, use_easyocr=False):#change to true if you want to use easyocr
    try:

        if file_path.lower().endswith(".pdf"):
            images = convert_from_path(file_path, dpi=300)
            if not images:
                return "Error: No images found in PDF."
            image = images[0]  # Use first page
            image.save(file_path.replace(".pdf", ".jpg"))  # Convert for OCR
            file_path = file_path.replace(".pdf", ".jpg")

        processed_image_path = preprocess_image(file_path)

        # Performs OCR with EasyOCR or Tesseract (added both incase one fails but currently only Tesseract is used)
        if use_easyocr:
            extracted_text = easyocr_extract_text(processed_image_path)
        else:
            extracted_text = pytesseract.image_to_string(
                Image.open(processed_image_path), lang="eng", config="--psm 4"
            )

        # Debugging Log - allows us to see the extracted text and check if it is empty
        print(f"🔎 Extracted Text:\n{extracted_text}")

        # Returns text if it is not empty or else returns an error message
        return (
            extracted_text if extracted_text.strip() else "Error: No text found in OCR."
        )

    except Exception as e:
        return f"Error processing file: {e}"


#  Extracts structured data from OCR text using Gemini AI
def generate_json_ai(text):
    try:
        if not text.strip() or len(text.split()) < 3:
            return {
                "error": "OCR output is too poor to process. Please try another image."
            }

        api_key = os.getenv("TOKEN_API_GEMINI")# Gemini API Key is stored in .env file
        if not api_key:
            raise ValueError("API Key is missing. Set TOKEN_API_GEMINI in .env")

        genai.configure(api_key=api_key) # configures the API key for Gemini AI
        #  Initializes the Gemini AI model
        model = genai.GenerativeModel("gemini-1.5-flash")

        #  Prompt for Gemini AI to convert text into structured JSON
        #  This is a basic prompt and can be improved with more specific instructions
        # prompt guidance can be found here: https://ai.google.dev/gemini-api/docs/structured-output?lang=python
        prompt = (
            "Analyze the extracted receipt text and convert it into structured JSON.\n"
            "Provide valid JSON output containing:\n"
            "- `establishment`: Name of the establishment\n"
            "- `date`: Date of the receipt\n"
            "- `items`: List of beverages and their prices\n"
            "- `total_price`: Total amount paid\n\n"
            f"Extracted text:\n{text}"
        )

        response = model.generate_content(prompt)# Generates content using the model based on the prompt

        #  Ensures AI response is not empty
        if not response.text.strip():
            return {"error": "Gemini AI returned an empty response."}

        # Ensures AI response is valid JSON
        try:
            clean_response = re.sub(r"```json|```", "", response.text).strip() #re.sub() removes the code block formatting
            #  This regex pattern removes any unwanted characters
            #  and ensures the JSON is properly formatted
            structured_data = json.loads(clean_response)
            return structured_data  # Return valid JSON
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse AI response: {e}",
                "raw_response": response.text,
            }

    except Exception as e:
        return {"error": f"Failed to generate structured data: {e}"}
