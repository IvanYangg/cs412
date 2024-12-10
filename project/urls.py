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
    path('register/', views.CreateUserProfileView.as_view(), name='register'),
    path('watchlist/', views.WatchlistView.as_view(), name='watchlist'),
    path('player/<int:pk>/add_to_watchlist/', views.AddToWatchlistView.as_view(), name='add_to_watchlist'),
    path('player/<int:pk>/remove_from_watchlist/', views.RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),
    path('social/', views.SocialPageView.as_view(), name='social'),
    path('social/my_posts/', views.MyPostsListView.as_view(), name='my_posts'),
    path('social/create/', views.CreatePostView.as_view(), name='create_post'),
    path('social/my_posts/update/<int:pk>/', views.UpdatePostView.as_view(), name='update_post'),
    path('social/my_posts/delete/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
]