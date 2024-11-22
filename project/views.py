from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Player, Team, Matchup

# Create your views here.

# List view for all matchups
class MatchupListView(ListView):
    model = Matchup
    template_name = "project/matchups.html"
    context_object_name = "matchups"

    def get_queryset(self):
        return Matchup.objects.all()

# List view for all players, and includes searching/filtering functionality
class PlayerListView(ListView):
    model = Player
    template_name = 'project/player_list.html'
    context_object_name = 'players'