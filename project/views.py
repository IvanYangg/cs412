from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Player, Team, Matchup

# Create your views here.

# List view for all matchups
class MatchupListView(ListView):
    model = Matchup
    template_name = "matchups.html"
    context_object_name = "matchups"

    def get_queryset(self):
        return Matchup.objects.all()

# List view for all players that are favorited/watchlisted by the user
class PlayerListView(ListView):
    model = Player
    template_name = 'player_list.html'
    context_object_name = 'players'