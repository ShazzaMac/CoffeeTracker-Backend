#OCR_API.py is responsible for managing HTTP requests, 
# calling utility functions, and returning responses.


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Avg
from mycoffeeapp.models import PriceEntry, ShopResult  # Ensure this is the correct import
import json
import uuid
from mycoffeeapp.ocr_utils import allowed_file, extract_text, generate_json_ai  # Import utility functions

@csrf_exempt
def upload_receipt(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]
        if not allowed_file(image_file.name):
            return JsonResponse({"error": "Invalid file format"}, status=400)
        
        unique_filename = f"uploads/{uuid.uuid4()}_{image_file.name}"
        file_path = default_storage.save(unique_filename, ContentFile(image_file.read()))
        
        try:
            # Use the utility function to extract text from the image
            extracted_text = extract_text(default_storage.open(file_path))
            
            if "Error" in extracted_text:
                return JsonResponse({"error": extracted_text}, status=500)
            
            # Process the text with AI to structure it into JSON
            extracted_data = generate_json_ai(extracted_text)
            
            shop_result = ShopResult.objects.create(json_data=json.dumps(extracted_data))
            return JsonResponse({"message": "OCR successful", "extracted_data": extracted_data, "id": shop_result.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
