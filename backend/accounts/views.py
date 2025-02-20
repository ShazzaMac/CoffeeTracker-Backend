# backend/accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def get_user_profile(request):
    """ Retrieve the profile data for the logged-in user """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def update_user_profile(request):
    """ Update the profile data for the logged-in user """
    try:
        # Ensure the request.user is authenticated
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Serialize the data to update the profile
    serializer = UserProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)  # Return updated profile data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
