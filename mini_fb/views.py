# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom views that are used within the application. 

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Profile

# Create your views here.
#custom view that shows all profiles 
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
    
#custom view to obtain data for one Profile record 
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'