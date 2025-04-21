#-------------------------------------------------------------------
# This file is used to register the UserProfile model in the Django admin interface.
#--------------------------------------------------------------------
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)
