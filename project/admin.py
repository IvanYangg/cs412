from django.contrib import admin
from .models import Player, Team, UserProfile, UserWatchList, PlayerGameLog, Matchup

# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(UserWatchList)
admin.site.register(PlayerGameLog)
admin.site.register(Matchup)
