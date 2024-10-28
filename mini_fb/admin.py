# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file registers all models used in the application


from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, Friend
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)
