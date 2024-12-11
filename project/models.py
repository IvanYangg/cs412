# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom models that are defined in my application. 
# Potential future updates include adding id, and player_img fields to the Player model, and comments, likes to the Post model to enhance the social experience. 

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Store season average data for a specific player
class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    minutes_per_game = models.FloatField()
    points_per_game = models.FloatField()
    assists_per_game = models.FloatField()
    rebounds_per_game = models.FloatField()
    three_pointers_per_game = models.CharField(max_length = 20)
    steals_per_game = models.FloatField()
    blocks_per_game = models.FloatField()
    turnovers_per_game = models.FloatField()
    fouls_per_game = models.FloatField()

# Store team data
class Team(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=3)
    avg_ppg = models.FloatField()
    avg_ppg_conceded = models.FloatField()
    avg_three_point_attempted = models.FloatField()
    avg_three_point_made = models.FloatField()
    avg_three_point_percentage = models.FloatField()
    avg_free_throw_attempted = models.FloatField()
    avg_rebounds_per_game = models.FloatField()
    avg_assists_per_game = models.FloatField()
    avg_steals_per_game = models.FloatField()
    avg_blocks_per_game = models.FloatField()
    avg_turnovers_per_game = models.FloatField()
    avg_fouls_per_game = models.FloatField()

# Provide a user profile for each user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Provide a list of players that a user is watching for easy access
class UserWatchList(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

# Provide game log data for a specific player
class PlayerGameLog(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    opponent = models.CharField(max_length=3)
    minutes = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    rebounds = models.IntegerField()
    three_pointers = models.CharField(max_length = 20)
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    fouls = models.IntegerField()

# Stores daily matchup data 
class Matchup(models.Model):
    team1 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='matchups_as_team1')
    team1_image_url = models.CharField(max_length=200)
    team2 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='matchups_as_team2')
    team2_image_url = models.CharField(max_length=200)
    
# Stores post data for users to interact with one another in social tab
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    message = models.TextField()
    image = models.ImageField(upload_to='social_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'