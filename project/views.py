from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Player, Team, Matchup, PlayerGameLog
from django.db.models import Q

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

    def get_queryset(self):
        # fetch all player records
        queryset = Player.objects.all()
        query = self.request.GET.get('query', '').strip()
        team = self.request.GET.get('team', '')
        sort_by = self.request.GET.getlist('sort_by', [])

        # Filter by name
        if query:
            queryset = queryset.filter(name__icontains=query)

        # Filter by team
        if team:
            queryset = queryset.filter(team__name=team)

        # Apply sorting based on the selected game stats
        if sort_by:
            for field in sort_by:
                queryset = queryset.order_by(f'-{field}')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        return context


# Detail view for a specific player, showing all game logs for that player
class PlayerDetailView(DetailView):
    model = Player
    template_name = "project/player_detail.html"
    context_object_name = "player"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_logs'] = PlayerGameLog.objects.filter(player=self.object).order_by('-date')
        context['player_averages'] = Player.objects.get(id=self.object.id)
        return context
    
# Watchlist view for a user, showing all players that the user is watching, restricted to logged in users
