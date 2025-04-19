# ------------------------------------------
# This file is used to register any models in the app with the 
# Django admin site, allowing them to be managed through the admin interface.
# This was originally intended to be set up to manage the ContactMessage model,
# which is used to store messages sent by users through the contact form.
# ------------------------------------------

from django.contrib import admin
from mycoffeeapp.models import ContactMessage

admin.site.site_header = "My Coffee App Admin" # Change the admin header
admin.site.site_title = "My Coffee App Admin Area" # Change the title of the admin area
admin.site.index_title = "Welcome to the My Coffee App Admin Area" # Change the index title

admin.site.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")
    search_fields = ("name", "email", "message")

