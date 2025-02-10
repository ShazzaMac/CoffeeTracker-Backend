from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core.mail import EmailMessage
import json
import os

def contact_form(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            message = data.get("message")

            # Validate input
            if not name or not email or not message:
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Create and send email
            email_message = EmailMessage(
                subject=f"New Contact Form Message from {name}",
                body=f"From: {name} ({email})\n\nMessage:\n{message}",
                from_email=os.getenv("EMAIL_USER"),  # Use your environment variable for the email
                reply_to=[email],
            )
            email_message.send(fail_silently=False)

            return JsonResponse({"success": "Message sent successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
