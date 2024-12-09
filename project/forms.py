from django import forms
from .models import UserProfile

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []
