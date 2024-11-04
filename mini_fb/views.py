# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom views that are used within the application. 

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add UserCreationForm to context
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # reconstruct the UserCreationForm from the POST data
        user_form = UserCreationForm(self.request.POST)
        # create the user and login
        user = user_form.save()
        form.instance.user = user
        # Log the user in after account creation
        login(self.request, user)
        # send to superclass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
#custom view to render form to create new status messages
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    # method for matching url to profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get profile from logged-in user
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context
    
    # validate the profile attribute and handle image uploads
    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile  
        # save the status message to database
        sm = form.save()
        # read the file from the form
        files = self.request.FILES.getlist('files')  
        for file in files:
            # associate image with status message
            image = Image(status_message=sm, image_file=file) 
            # save the image to the database 
            image.save()  
        return super().form_valid(form)
    
    # handle redirection of url after submission of new status form
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

#custom view to update profile
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    # handle redirection of url after a successful update
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

# custom view for deleting status messages
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_object(self):
        return get_object_or_404(StatusMessage, pk=self.kwargs['pk'], profile__user=self.request.user)
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

# custom view for updating status messages
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_object(self):
        return get_object_or_404(StatusMessage, pk=self.kwargs['pk'], profile__user=self.request.user)
    
    # handle redirection of url after updating status message
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

# custom view for adding friends
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

# custom view for showing friend suggestions
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context

# custom view for showing news feed
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context
    
