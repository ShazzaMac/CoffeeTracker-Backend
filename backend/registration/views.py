# ----------------------------------------------------------
# This file contains the views for user registration, login,
# password reset, and other authentication-related functionalities.
# ----------------------------------------------------------

import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, Count
from django.http import JsonResponse, QueryDict
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CoffeeShop
from .serializers import UserLoginSerializer, UserRegistrationSerializer

# Initialize logger
logger = logging.getLogger(__name__)


# Helper to generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# +-----------------------------------------------------+
#                    USER REGISTRATION VIEWS
# +-----------------------------------------------------+
# This view handles user registration, including validation and token generation.
# It uses Django's built-in authentication system to create a new user and send a welcome email.
# It also includes a login view for user authentication and a password reset view.
# The views are protected by rate limiting to prevent abuse.
# The views are designed to be used with Django REST Framework and include appropriate permissions.
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(f"Received registration data: {request.data}")

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            logger.info("User created successfully")
            return Response(
                {
                    "message": "User created successfully",
                    "tokens": tokens,
                    "username": user.username,
                },
                status=status.HTTP_201_CREATED,
            )

        logger.error(f"Registration errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# +-----------------------------------------------------+
#                    LOGIN VIEW
# +-----------------------------------------------------+
# This view handles user login, including validation and token generation.
# It uses Django's built-in authentication system to authenticate the user.
# It also includes a password reset view that sends a temporary password to the user's email.
# The views are protected by rate limiting to prevent abuse.
@method_decorator(
    ratelimit(key="ip", rate="3/m", method="POST", block=True), name="dispatch"
)  # the ratelimit decorator is used to limit the number of requests to this view to 3 per minute
# This is useful to prevent brute-force attacks on the login endpoint


class LoginView(APIView):
    def post(self, request):
        logger.info(f"Login attempt with raw data: {request.data}")

        data = (
            request.data.dict() if isinstance(request.data, QueryDict) else request.data
        )
        logger.info(f"Processed login data: {data}")

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            logger.error("Username or password missing")
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user:
            # CREATE THE DRF TOKEN HERE -- currently using jwt
            # token, _ = Token.objects.get_or_create(user=user)

            tokens = get_tokens_for_user(user)
            logger.info(f"Login successful for user: {username}")

            return Response(
                {
                    "message": "Login successful",
                    "tokens": tokens,
                    # "drf_token": token.key,
                    "username": user.username,
                },
                status=status.HTTP_200_OK,
            )

        logger.error(f"Login failed: Invalid credentials for username {username}")
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


# This view handles password reset requests.
# It sends a temporary password to the user's email address.
# The view checks if the email exists in the database and sends a new password if it does.
# If the email does not exist, it returns a 404 error.
# The view is protected by rate limiting to prevent abuse.
@method_decorator(
    ratelimit(key="ip", rate="5/m", method="POST", block=True), name="dispatch"
)
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            new_password = get_random_string(length=12)
            user.set_password(new_password)
            user.save()

            send_mail(
                "Your New Password",
                f"Your new temporary password is: {new_password}\nPlease log in and change it immediately.",
                "From the CoffeeTrackerApp Team",
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


# This view handles password reset requests.
# It checks if the token is valid and resets the password if it is.
# The view checks if the user exists and if the token is valid.
# If the token is invalid or expired, it returns a 400 error.
# If the user does not exist, it returns a 404 error.


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        try:
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


def custom_ratelimited(request, exception=None):
    return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)


class ProtectedEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})


class DashboardView(View):
    def get(self, request):
        return JsonResponse({"message": "Welcome to the dashboard!"})


# APIView for coffee shop statistics -- consider moving to main folder
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
