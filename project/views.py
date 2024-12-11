# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom views that are implemented in my application.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Player, Team, Matchup, PlayerGameLog, UserWatchList, UserProfile, Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateProfileForm, PostForm
from django.db.models import Q

# Create your views here.

# List view for all matchups
class MatchupListView(ListView):
    model = Matchup
    template_name = "project/matchups.html"
    context_object_name = "matchups"

    # Fetch all matchup records
    def get_queryset(self):
        return Matchup.objects.all()

# Detail view for a specific matchup, and reveals both teams statistics side by side
class MatchupDetailView(DetailView):
    model = Matchup
    template_name = "project/matchup_detail.html"
    context_object_name = "matchup"

# List view for all players, and includes searching/filtering functionality
class PlayerListView(ListView):
    model = Player
    template_name = 'project/player_list.html'
    context_object_name = 'players'

    def get_queryset(self):
        # fetch all player records
        queryset = Player.objects.all()
        query = self.request.GET.get('query', '').strip()
        team = self.request.GET.get('team', '')
        sort_by = self.request.GET.get('sort_by', '')

        # name filter
        if query:
            queryset = queryset.filter(name__istartswith=query)

        # team filter
        if team:
            queryset = queryset.filter(team__name=team)

        # Sort based on selected game stat
        if sort_by:
            queryset = queryset.order_by(f'-{sort_by}')

        return queryset

    # obtain all teams for the filter dropdown
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        return context

# Detail view for a specific player, showing all game logs for that player
class PlayerDetailView(DetailView):
    model = Player
    template_name = "project/player_detail.html"
    context_object_name = "player"

    # context for fetching game logs and player averages, as well as checking if the player is in the user's watchlist 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_logs'] = PlayerGameLog.objects.filter(player=self.object).order_by('-date')
        context['player_averages'] = Player.objects.get(id=self.object.id)
        player = context['player']
        if self.request.user.is_authenticated:
            user_profile = self.request.user.userprofile
            context['in_watchlist'] = UserWatchList.objects.filter(user=user_profile, player=player).exists()
        return context

# Registration view for new users
class CreateUserProfileView(CreateView):
    model = UserProfile
    form_class = CreateProfileForm
    template_name = 'project/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add UserCreationForm to context
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Reconstruct the UserCreationForm from the POST data
        user_form = UserCreationForm(self.request.POST)
        # Create the user and login
        user = user_form.save()
        form.instance.user = user
        # Log the user in after account creation
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('matchups')

# Watchlist view for a user, showing all players that the user is watching, restricted to logged in users
class WatchlistView(LoginRequiredMixin, ListView):
    model = UserWatchList
    template_name = 'project/watchlist.html' 
    context_object_name = 'watchlist'

    # Fetch all players in the user's watchlist
    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return UserWatchList.objects.filter(user=user_profile)

# Add player to watchlist
class AddToWatchlistView(LoginRequiredMixin, CreateView):
    model = UserWatchList
    fields = []
    template_name = 'project/add_to_watchlist.html'

    # this function is used to pass the player object, if it exists, to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = get_object_or_404(Player, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # Get the player and user profile
        player = get_object_or_404(Player, pk=self.kwargs['pk'])
        user_profile = self.request.user.userprofile

        # Check if the player is already in the user's watchlist
        if not UserWatchList.objects.filter(user=user_profile, player=player).exists():
            form.instance.user = user_profile
            form.instance.player = player
            return super().form_valid(form)

    # Handle redirection
    def get_success_url(self):
        return reverse('watchlist')

# Remove player from watchlist
class RemoveFromWatchlistView(LoginRequiredMixin, DeleteView):
    model = UserWatchList
    template_name = 'project/remove_from_watchlist.html'

    def get_object(self):   
        # Get the player object and the user’s watchlist entry
        player = get_object_or_404(Player, pk=self.kwargs['pk'])
        user_profile = self.request.user.userprofile
        return get_object_or_404(UserWatchList, user=user_profile, player=player)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the player to context
        context['player'] = self.get_object().player
        return context

    # Handle redirection
    def get_success_url(self):
        return reverse('watchlist')
    
# List view for all posts/social page
class SocialPageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'project/social.html'
    context_object_name = 'posts'

    # Fetch all posts and order by timestamp
    def get_queryset(self):
        return Post.objects.all().order_by('-timestamp')

# Create view for new posts
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'project/create_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate the post with the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('social')
    
# View for page showing all posts that a logged-in user has made, landing page for making edits and deletions to posts
class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'project/my_posts.html'
    context_object_name = 'posts'

    # Fetch all posts that the logged-in user has made and order by timestamp
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-timestamp')

# View for updating posts that a logged-in user has made
class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'project/update_post.html'

    def get_queryset(self):
        # Ensure only the author can update their own posts
        return Post.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse('social')

# View for deleting posts that a logged-in user has made
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'project/delete_post.html'

    def get_queryset(self):
        # Ensure only the author can delete their own posts
        return Post.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse('social')