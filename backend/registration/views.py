# registration/views.py (for API-based registration)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer  # Your serializer that handles user registration


import logging
logger = logging.getLogger(__name__)

class UserRegistrationView(APIView):
    def post(self, request):
        logger.info(f"Received data: {request.data}")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("User created successfully")
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        logger.error(f"Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
