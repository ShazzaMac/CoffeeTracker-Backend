# Import necessary modules
import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, Count
from django.http import JsonResponse, HttpResponseBadRequest, QueryDict
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CoffeeShop
from .serializers import UserLoginSerializer, UserRegistrationSerializer

# +-----------------------------------------------------+
# Initialize logger
logger = logging.getLogger(__name__)
# +-----------------------------------------------------+


# This view is used to register a new user
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(f"Received registration data: {request.data}")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            logger.info("User created successfully")
            return Response(
                {"message": "User created successfully", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        logger.error(f"Registration errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# +-----------------------------------------------------+

class LoginView(APIView):
    def post(self, request):
        logger.info(f"Login attempt with raw data: {request.data}")

        # Convert QueryDict to a normal dictionary
        data = request.data.dict() if isinstance(request.data, QueryDict) else request.data
        logger.info(f"Processed login data: {data}")

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            if not password:
                logger.error("Password field missing after serializer validation")
                return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                logger.info(f"Login successful for user: {username}")
                return Response(
                    {"message": "Login successful", "token": token.key},
                    status=status.HTTP_200_OK,
                )
            else:
                logger.error(f"Login failed: Invalid credentials for username {username}")
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        logger.error(f"Login validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# +-----------------------------------------------------+

# This view is used to send a password reset link to the user's email
@method_decorator(
    ratelimit(key="ip", rate="5/m", method="POST", block=True), name="dispatch"
)
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]  # Allow any user, even unauthenticated users

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)

            # Generates a new secure password of 12 characters
            new_password = get_random_string(length=12)

            # Set the new password for the user
            user.set_password(new_password)
            user.save()

            # Send the email with the new password
            send_mail(
                "Your New Password",
                f"Your new temporary password is: {new_password}\nPlease log in and change it immediately.",
                "From the CoffeeTrackerApp Team",  # Replace with your sender email
                [email],
            )
            logger.info(f"Password reset email sent to {email} with a new password.")
            return Response(
                {"message": "A new password has been sent to your email."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "No user with this email exists. Please try again"},
                status=status.HTTP_404_NOT_FOUND,
            )

# +-----------------------------------------------------+

# This view is used to reset the user's password
class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        try:
            # Decode the UID and check token
            user = User.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                return JsonResponse(
                    {"error": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_password = request.data.get("password")
            user.set_password(new_password)
            user.save()
            return JsonResponse(
                {"message": "Password reset successfully."}, status=status.HTTP_200_OK
            )
        except (User.DoesNotExist, ValueError):
            return JsonResponse(
                {"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST
            )


from django.http import JsonResponse


def custom_ratelimited(request, exception=None):
    return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)

# +-----------------------------------------------------+


class ProtectedEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})

# +-----------------------------------------------------+

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]


class DashboardView(View):
    def get(self, request):
        return JsonResponse({"message": "Welcome to the dashboard!"})

    def get(self, request):
        return Response({"message": "Welcome to your dashboard!"})

# +-----------------------------------------------------+

class CoffeeStatsAPIView(APIView):
    def get(self, request):
        total_shops = CoffeeShop.objects.count()
        if total_shops == 0:
            return Response(
                {"message": "No coffee shop data available."}, status=status.HTTP_200_OK
            )

        avg_price = CoffeeShop.objects.aggregate(Avg("price"))["price__avg"]
        most_popular = (
            CoffeeShop.objects.values("coffee_type")
            .annotate(count=Count("coffee_type"))
            .order_by("-count")
            .first()
        )
        most_popular_coffee = most_popular["coffee_type"] if most_popular else None

        data = {
            "total_shops": total_shops,
            "avg_price": avg_price,
            "most_popular_coffee": most_popular_coffee,
        }
        return Response(data, status=status.HTTP_200_OK)
