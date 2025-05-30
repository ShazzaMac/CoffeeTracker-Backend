# --------------------------------------------------------------
# these views are used to handle user profile updates and password changes
# --------------------------------------------------------------
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, PasswordChangeSerializer


# ProfileUpdateView handles the retrieval and update of user profiles.
# It uses the UserProfileSerializer to serialize the user data.
# The get method retrieves the user's profile data, while the patch method updates it.
class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The PasswordChangeView handles password changes for authenticated users.
class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data["current_password"]
            new_password = serializer.validated_data["new_password"]

            if not user.check_password(current_password):
                return Response(
                    {"detail": "Current password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
