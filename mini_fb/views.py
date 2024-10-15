# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom views that are used within the application. 

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm

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

#custom view to render the form to create new profiles
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html' 

#custom view to render form to create new status messages
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    # method for matching url to profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # find pk from the URL
        pk = self.kwargs['pk']
        # match corresponding profile
        profile = Profile.objects.get(pk=pk)
        # add profile to context data
        context['profile'] = profile
        return context
    
    # validate the profile attribute
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])  
        form.instance.profile = profile  
        return super().form_valid(form)
    
    # handle redirection of url after submission of new status form
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})