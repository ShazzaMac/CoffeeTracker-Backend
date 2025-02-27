# This file is used to register the models in the admin panel. To do this,
# you need to import the models and register them using the admin.site.register() method.
from django.contrib import admin
from mycoffeeapp.models import ContactMessage

admin.site.site_header = "My Coffee App Admin" # Change the admin header
admin.site.site_title = "My Coffee App Admin Area" # Change the title of the admin area
admin.site.index_title = "Welcome to the My Coffee App Admin Area" # Change the index title

admin.site.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")
    search_fields = ("name", "email", "message")

