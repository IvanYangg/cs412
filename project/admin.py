# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the models that are registered in my application. 

from django.contrib import admin
from .models import Player, Team, UserProfile, UserWatchList, PlayerGameLog, Matchup, Post

# Register your models here.
admin.site.register(Player)
admin.site.register(UserProfile)
admin.site.register(UserWatchList)
admin.site.register(Team)
admin.site.register(PlayerGameLog)
admin.site.register(Matchup)
admin.site.register(Post)
