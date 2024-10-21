# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines the forms used in this application

# mini_fb/forms.py
from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
        
class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']