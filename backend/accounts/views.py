# backend/accounts/views.py
from profile import Profile
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView




@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        return JsonResponse({
            'username': profile.user.username,
            'email': profile.user.email,
            'phone': profile.phone,
            'about': profile.about,
            'profilePhoto': profile.profile_photo.url if profile.profile_photo else None,
        })
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

@csrf_exempt
@login_required
def update_profile(request):
    if request.method == 'POST':
        data = request.json()
        profile = Profile.objects.get(user=request.user)
        profile.phone = data.get("phone", profile.phone)
        profile.about = data.get("about", profile.about)
        profile.save()
        return JsonResponse({"message": "Profile updated successfully"})

@csrf_exempt
@login_required
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        profile = Profile.objects.get(user=request.user)
        profile.profile_photo = request.FILES['photo']
        profile.save()
        return JsonResponse({
            'profilePhoto': profile.profile_photo.url
        })
    return JsonResponse({"error": "Failed to upload photo"}, status=400)

