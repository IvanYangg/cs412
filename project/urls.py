from django.urls import path
from . import views

urlpatterns = [
    path('matchups/', views.MatchupListView.as_view(), name='matchups'),
    path('matchup/<int:pk>/', views.MatchupDetailView.as_view(), name='matchup_detail'),
    path('players/', views.PlayerListView.as_view(), name='players'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
]