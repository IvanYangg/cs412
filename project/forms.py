# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines the custom forms that are defined in my project application. 

from django import forms
from .models import UserProfile, Post

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', 'image']
