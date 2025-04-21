# ---------------------------------------------------------------------
# This file is used to handle OCR extraction from uploaded receipt images.
# It uses Django's default storage to save the uploaded image and then
# processes it to extract text and generate structured data.
# ----------------------------------------------------------------------------
import json
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from .utils import extract_text, generate_json_ai


@csrf_exempt
def ocr_extract(request):
    """Handles OCR extraction from uploaded receipt images."""
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]
        path = default_storage.save(
            f"receipts/{image_file.name}", ContentFile(image_file.read())
        )

        extracted_text = extract_text(default_storage.path(path))
        structured_data = generate_json_ai(extracted_text)

        return JsonResponse(
            {"extracted_text": extracted_text, "structured_data": structured_data}
        )

    return JsonResponse({"error": "No image provided"}, status=400)
