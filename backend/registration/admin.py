# This file is used to register the models in the admin panel. To do this,
# you need to import the models and register them using the admin.site.register() method.
from django.contrib import admin
from mycoffeeapp.models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "created_at")
    search_fields = ("name", "email", "message")

