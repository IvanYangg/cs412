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
    three_pointers_made_per_game = models.FloatField()
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
    minutes = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    rebounds = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    fouls = models.IntegerField()

# Stores daily matchup data 
class Matchup(models.Model):
    team1 = models.CharField(max_length=50)
    team1_image_url = models.CharField(max_length=200)
    team2 = models.CharField(max_length=50)
    team2_image_url = models.CharField(max_length=200)
