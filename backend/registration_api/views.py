import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_ratelimit.decorators import ratelimit

from .models import CoffeeShop
from .serializers import UserLoginSerializer, UserRegistrationSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})
    
    
# Initialize logger
logger = logging.getLogger(__name__)

# User Registration View
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

# Login View
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                # Create or get a token for the user
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "message": "Login successful",
                        "token": token.key,  # Return the token to the client
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Forgot Password View
@method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True), name="dispatch")
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

# Reset Password View
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

# Dashboard View (API-based)
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome to your dashboard!"})

# Coffee Stats View
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
