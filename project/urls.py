from django.urls import path
from . import views

urlpatterns = [
    path('matchups/', views.MatchupListView.as_view(), name='matchups'),
    path('players/', views.PlayerListView.as_view(), name='player_list'),
]