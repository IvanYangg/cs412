from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('matchups/', views.MatchupListView.as_view(), name='matchups'),
    path('matchup/<int:pk>/', views.MatchupDetailView.as_view(), name='matchup_detail'),
    path('players/', views.PlayerListView.as_view(), name='players'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]