# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file registers all models used in the application


from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage
admin.site.register(Profile)
admin.site.register(StatusMessage)
