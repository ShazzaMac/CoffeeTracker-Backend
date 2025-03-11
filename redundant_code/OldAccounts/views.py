from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveUpdateAPIView
from django.http import JsonResponse
from rest_framework.exceptions import NotFound



# ---------------------------------------------------------------
# API Views
# ---------------------------------------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    # Ensure we fetch the correct profile
    profile, created = UserProfile.objects.get_or_create(username=user.username)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_photo(request):
    user = request.user

    try:
        profile, created = UserProfile.objects.get_or_create(username=user.username)
        
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
            profile.save()
            return Response({'message': 'Profile photo uploaded successfully'})
        
        return Response({'error': 'Profile photo not uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)



# ---------------------------------------------------------------
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        # Fetch the profile object
        user_profile = request.user.profile

        # Serialize and update
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the user's profile
        profile = request.user.userprofile

        # Serialize the data (you can manually serialize or use Django Rest Framework serializers)
        profile_data = {
            "username": profile.username,
            "email": profile.email,
            "phone": profile.phone,
            "about": profile.about,
            "profile_photo": profile.profile_photo.url if profile.profile_photo else None,
        }

        return JsonResponse(profile_data)