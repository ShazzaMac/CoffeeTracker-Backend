from django.core.mail import send_mail
from django.conf import settings

def send_contact_email(name, email, message):
    """
    Sends an email when a user submits a contact form.
    """
    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_email = ["coffeetrackerapphelp@gmail.com"]

    try:
        send_mail(subject, body, sender_email, recipient_email)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
