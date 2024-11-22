from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Player, Team, Matchup, PlayerGameLog

# Create your views here.

# List view for all matchups
class MatchupListView(ListView):
    model = Matchup
    template_name = "project/matchups.html"
    context_object_name = "matchups"

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

# Detail view for a specific player, showing all game logs for that player
class PlayerDetailView(DetailView):
    model = Player
    template_name = "project/player_detail.html"
    context_object_name = "player"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_logs'] = PlayerGameLog.objects.filter(player=self.object).order_by('-date')
        return context