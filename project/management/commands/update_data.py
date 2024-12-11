# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines the custom management command script that fetches NBA data from ESPN API and updates the database. Although not automated yet, this file will eventually be run daily, perhaps around 2am when all games have long finished, to retrieve bulk data from the ESPN API. The data is then parsed and stored in the database. The script is divided into three main functions: update_teams, update_matchups, and update_players. The update_teams function fetches NBA team data and stores it in the Team model. The update_matchups function fetches NBA matchup data and stores it in the Matchup model. The update_players function fetches NBA player data and stores it in the Player and PlayerGameLog models. The script also includes a clear_data function that wipes all data from the database to prevent duplicates. The script uses the requests library to make HTTP requests to the ESPN API and the time library to introduce delays between requests to avoid rate limiting. This script is executed by running the command 'python manage.py update_data' in the terminal.

# Future progress for this script: 
# 1. Automate the script to run daily at a specific time.
# 2. More error-logging/checking because there is a lot of data being loaded in. 
# 3. Right now the script takes about 30 minutes to update all the data. This can be optimized by instead of fetching data for all players, only fetching data for players that have played a game that day, utilizing the matchups data to determine which players have played. This can also be further optimized by not rewriting the entire player gamelog data every time, but only adding the data for the most recent games, or the topmost game of the player log because the ESPN API displays games chronologically e.g. something like this events[0].
# 4. Masking the API call
# 5. Fetching player images as well, and perhaps their ids to make the code cleaner. 
# 6. Moving the list of players to a separate file to make the code cleaner.

import time
import requests
from django.core.management.base import BaseCommand
from project.models import Team, Player, PlayerGameLog, Matchup
from django.utils import timezone


class Command(BaseCommand):
    help = "Fetch daily NBA data and update the database"

    def handle(self, *args, **kwargs):
        self.clear_data()
        self.stdout.write("Starting data update...")
        self.update_teams()
        time.sleep(10)
        self.update_matchups()
        time.sleep(10)
        self.update_players()
        self.stdout.write("All Data successfully updated!")
        
    def clear_data(self):
        #wipe all data to prevent duplicates 
        self.stdout.write("Clearing existing matchup data...")
        Matchup.objects.all().delete()
        self.stdout.write("Clearing existing team data...")
        Team.objects.all().delete()
        self.stdout.write("Clearing existing player game log data...")
        PlayerGameLog.objects.all().delete()
        
    def update_teams(self):
        """Fetch and update NBA team data."""
        self.stdout.write("Updating teams...")
        """ need to mask the api key """
        team_url = "https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/statistics/byteam?region=us&lang=en&contentorigin=espn"
        
        try:
            teams_data = requests.get(team_url).json()
            for team in teams_data["teams"]:
                # obtain statistics for each team
                for split in team["categories"]:
                    if split["name"] == "general" and split["displayName"] == "Own General":
                        reb = split["totals"][1]
                        pf = split["totals"][8]
                    elif split["name"] == "defensive" and split["displayName"] == "Own Defensive":
                        steals = split["totals"][2]  
                        blocks = split["totals"][3]
                    elif split["name"] == "offensive" and split["displayName"] == "Own Offensive":
                        pts = split["totals"][0]  
                        turnovers = split["totals"][4]
                        three_point_percentage = split["totals"][2]
                        three_point_made = split["totals"][8]
                        three_point_attempted = split["totals"][9]
                        ft_attempted = split["totals"][11]
                        assists = split["totals"][13]
                    elif split["name"] == "offensive" and split["displayName"] == "Opponent Offensive":
                        ppg_conceded = split["totals"][0]
                        
                # create the team object
                teamData = Team(
                    name = team["team"]["displayName"],
                    abbreviation = team["team"]["abbreviation"],
                    avg_ppg = pts,
                    avg_ppg_conceded = ppg_conceded,
                    avg_three_point_attempted = three_point_attempted,
                    avg_three_point_made = three_point_made,
                    avg_three_point_percentage = three_point_percentage,
                    avg_free_throw_attempted = ft_attempted,
                    avg_rebounds_per_game = reb,
                    avg_assists_per_game = assists,
                    avg_steals_per_game = steals,
                    avg_blocks_per_game = blocks,
                    avg_turnovers_per_game = turnovers,
                    avg_fouls_per_game = pf
                )
                teamData.save() #save to database
                
            self.stdout.write("Teams updated successfully.")
        except requests.exceptions.RequestException as e:
            self.stdout.write(f"Error updating teams: {e}")
         
    def update_matchups(self):
        """ Fetch and update NBA matchup data."""
        self.stdout.write("Updating matchups...")
        today = timezone.now().date()
        formatted_today = today.strftime("%Y%m%d")
        url = f"https://site.web.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?region=us&lang=en&contentorigin=espn&limit=100&calendartype=offdays&includeModules=videos&dates={formatted_today}&tz=America%2FNew_York"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                self.stderr.write(f"Failed to fetch data for {today}. HTTP Status: {response.status_code}")
                return
            
            data = response.json()
            for event in data["events"]:
                team1 = event["competitions"][0]["competitors"][0]["team"]
                team2 = event["competitions"][0]["competitors"][1]["team"]
                #extract foreign key teams objects
                team1_obj = Team.objects.get(abbreviation=team1["abbreviation"])
                team2_obj = Team.objects.get(abbreviation=team2["abbreviation"])
                #create matchup object
                matchup = Matchup(
                    team1 = team1_obj,
                    team1_image_url = team1["logo"],
                    team2 = team2_obj,
                    team2_image_url = team2["logo"]
                )
                matchup.save() #save to database
            self.stdout.write(f"Matchups for {today} successfully updated.")
        except requests.exceptions.RequestException as e:
            self.stdout.write(f"Error updating matchups: {e}")
           
    def update_players(self):
        """Fetch and update NBA player data."""
        self.stdout.write("Updating players...") 
        
        #players that my app tracks [id, name, abbreviation of team, position]
        #Warriors is GS, Knicks is NY, Pelicans is NO, Spurs is SA, Jazz is UTAH
        players = [[4065648, "Jayson Tatum", "BOS", "SF"], [4396971, "Naz Reid", "MIN", "C"], [3112335, "Nikola Jokic", "DEN", "C"], [3945274, "Luka Doncic", "DAL", "PG"], [2991043, "Caris LeVert", "CLE", "SG"], [4897943, "Dalton Knecht", "LAL", "G"], [3917376, "Jaylen Brown", "BOS", "SG"], [3934719, "OG Anunoby", "NY", "SF"], [4593803, "Jalen Williams", "OKC", "F"], [3032976, "Rudy Gobert", "MIN", "C"], [3995, "Jrue Holiday", "BOS", "PG"], [4066457, "Austin Reaves", "LAL", "SG"], [4278078, "P.J. Washington", "DAL", "PF"], [4278104, "Michael Porter Jr.", "DEN", "SF"], [2990969, "Georges Niang", "CLE", "SF"], [3064514, "Julius Randle", "MIN", "PF"], [3147657, "Mikal Bridges", "NY", "SF"], [4278049, "Daniel Gafford", "DAL", "C"], [4066354, "Payton Pritchard", "BOS", "PG"], [3078576, "Derrick White", "BOS", "PG"], [4432158, "Evan Mobley", "CLE", "PF"], [3136195, "Karl-Anthony Towns", "NY", "C"], [4396907, "Darius Garland", "CLE", "PG"], [4222252, "Isaiah Hartenstein", "OKC", "C"], [3136776, "D'Angelo Russell", "LAL", "PG"], [3936299, "Jamal Murray", "DEN", "PG"], [3102531, "Kristaps Porzingis", "BOS", "C"], [3213, "Al Horford", "BOS", "C"], [4066648, "Rui Hachimura", "LAL", "PF"], [4065804, "Sam Hauser", "BOS", "SF"], [4594268, "Anthony Edwards", "MIN", "SG"], [4278073, "Shai Gilgeous-Alexander", "OKC", "PG"], [3468, "Russell Westbrook", "DEN", "PG"], [3064560, "Luke Kornet", "BOS", "C"], [4431767, "Christian Braun", "DEN", "G"], [3064290, "Aaron Gordon", "DEN", "PF"], [3195, "Mike Conley", "MIN", "PG"], [6442, "Kyrie Irving", "DAL", "PG"], [4431671, "Jaden Mcdaniels", "MIN", "PF"], [3934673, "Donte Divincenzo", "MIN", "SG"], [3102529, "Clint Capela", "ATL", "C"], [3062679, "Josh Hart", "NY", "SG"], [1966, "Lebron James", "LAL", "SF"], [4397020, "Lugentz Dort", "OKC", "G"], [3934672, "Jalen Brunson", "NY", "PG"], [4066328, "Jarrett Allen", "CLE", "C"], [6475, "Klay Thompson", "DAL", "SG"], [6583, "Anthony Davis", "LAL", "PF"], [4017837, "Ivica Zubac", "LAC", "C"], [3908809, "Donovan Mitchell", "CLE", "SG"], [3155526, "Dillon Brooks", "HOU", "SF"], [4683634, "Bennedict Mathurin", "IND", "SG"], [4437244, "Jalen Green", "HOU", "SG"], [4871144, "Alperen Sengun", "HOU", "C"], [4277905, "Trae Young", "ATL", "PG"], [2991230, "Fred VanVleet", "HOU", "PG"], [4433192, "Tari Eason", "HOU", "F"], [4684740, "Amen Thompson", "HOU", "F"], [4593125, "Santi Aldama", "MEM", "PF"], [4066320, "Desmond Bane", "MEM", "SG"], [4277961, "Jaren Jackson Jr.", "MEM", "PF"], [4869342, "Dyson Daniels", "ATL", "G"], [4279888, "Ja Morant", "MEM", "PG"], [3913176, "Brandon Ingram", "NO", "SF"], [3907497, "Dejounte Murray", "NO", "SG"], [4066262, "Malik Monk", "SAC", "SG"], [4397688, "Trey Murphy III", "NO", "SG"], [4277813, "Herbert Jones", "NO", "SF"], [6578, "Harrison Barnes", "SA", "SF"], [3155942, "Domantas Sabonis", "SAC", "PF"], [4845367, "Stephon Castle", "SA", "G"], [4396993, "Tyrese Haliburton", "IND", "PG"], [4592479, "Julian Champagnie", "SA", "F"], [2779, "Chris Paul", "SA", "PG"], [4594327, "Keegan Murray", "SAC", "SF"], [5104157, "Victor Wembanyama", "SA", "C"], [4871145, "Josh Giddey", "CHI", "SG"], [3064440, "Zach LaVine", "CHI", "SG"], [4395651, "Coby White", "CHI", "PG"], [4701230, "Jalen Johnson", "ATL", "SF"], [4397002, "Ayo Dosunmu", "CHI", "SG"], [3978, "DeMar DeRozan", "SAC", "SF"], [6478, "Nikola Vucevic", "CHI", "C"], [4066259, "De'Aaron Fox", "SAC", "PG"], [3149673, "Pascal Siakam", "IND", "PF"], [3133628, "Myles Turner", "IND", "C"], [3975, "Stephen Curry", "GS", "PG"], [6589, "Draymond Green", "GS", "PF"], [4433247, "Jonathan Kuminga", "GS", "PF"], [2990984, "Buddy Hield", "GS", "SG"], [3059319, "Andrew Wiggins", "GS", "SF"], [3032977, "Giannis Antetokounmpo", "MIL", "PF"], [6606, "Damian Lillard", "MIL", "PG"], [3448, "Brook Lopez", "MIL", "C"], [3064482, "Bobby Portis", "MIL", "F"], [6609, "Khris Middleton", "MIL", "SF"], [6580, "Bradley Beal", "PHX", "SG"], [3136193, "Devin Booker", "PHX", "SG"], [3202, "Kevin Durant", "PHX", "PF"], [3135046, "Tyus Jones", "PHX", "PG"], [3102530, "Jusuf Nurkic", "PHX", "C"], [3135045, "Grayson Allen", "PHX", "SG"], [4433134, "Scottie Barnes", "TOR", "SF"], [4395625, "RJ Barrett", "TOR", "SG"], [5106258, "Gradey Dick", "TOR", "G"], [3134908, "Jakob Poeltl", "TOR", "C"], [4278053, "Davion Mitchell", "TOR", "PG"], [4066261, "Bam Adebayo", "MIA", "C"], [6430, "Jimmy Butler", "MIA", "SF"], [4395725, "Tyler Herro", "MIA", "PG"], [3157465, "Duncan Robinson", "MIA", "F"], [3074752, "Terry Rozier", "MIA", "SG"], [3907822, "Malik Beasley", "DET", "SG"], [4432166, "Cade Cunningham", "DET", "PG"], [6440, "Tobias Harris", "DET", "F"], [4433218, "Jaden Ivey", "DET", "PG"], [4433621, "Jalen Duren", "DET", "C"], [4278067, "Nic Claxton", "BKN", "C"], [3138196, "Cameron Johnson", "BKN", "SF"], [3032979, "Dennis Schroder", "BKN", "PG"], [3907387, "Ben Simmons", "BKN", "PG"], [2578185, "Dorian Finney-Smith", "BKN", "PF"], [3908845, "John Collins", "UTAH", "PF"], [4066336, "Lauri Markkanen", "UTAH", "PF"], [4277811, "Collin Sexton", "UTAH", "PG"], [2528426, "Jordan Clarkson", "UTAH", "PG"], [4433627, "Keyonte George", "UTAH", "G"], [3992, "James Harden", "LAC", "SG"], [2595516, "Norman Powell", "LAC", "G"], [4277956, "Jordan Poole", "WSH", "SG"], [3134907, "Kyle Kuzma", "WSH", "SF"], [2566769, "Malcolm Brogdon", "WSH", "PG"], [5104155, "Bilal Coulibaly", "WSH", "SG"], [4348700, "Goga Bitadze", "ORL", "C"], [4566434, "Franz Wagner", "ORL", "SF"], [3150844, "Moritz Wagner", "ORL", "C"], [4432165, "Jalen Suggs", "ORL", "SG"], [2581018, "Kentavious Caldwell-Pope", "ORL", "SG"], [4277847, "Wendell Carter Jr.", "ORL", "C"], [4432816, "LaMelo Ball", "CHA", "PG"], [4066383, "Miles Bridges", "CHA", "SF"], [4432811, "Josh Green", "CHA", "SG"], [4433287, "Brandon Miller", "CHA", "F"], [4683021, "Deni Avdija", "POR", "SF"], [4278129, "Deandre Ayton", "POR", "C"], [2991070, "Jerami Grant", "POR", "SF"], [4683678, "Scoot Henderson", "POR", "G"], [4914336, "Shaedon Sharpe", "POR", "SG"], [4351851, "Anfernee Simons", "POR", "SG"], [3059318, "Joel Embiid", "PHI", "C"], [4251, "Paul George", "PHI", "F"], [4431678, "Tyrese Maxey", "PHI", "PG"], [4683778, "Jared McCain", "PHI", "G"], [3133603, "Kelly Oubre Jr.", "PHI", "SG"]]

        try: 
            for player in players:
                id, name, team, pos = player
                self.stdout.write(f"Fetching data for {name}...")
                time.sleep(10) # wait for 10 seconds to avoid rate limiting
                # team is a foreign-key relationship so we need to fetch the team object
                team_obj = Team.objects.get(abbreviation=team)
                
                # Dynamically construct URL
                url = f"https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/{id}/gamelog?region=us&lang=en&contentorigin=espn"
                response = requests.get(url)
                
                # Handle potential HTTP errors
                if response.status_code != 200:
                    self.stderr.write(f"Failed to fetch data for {name} (ID: {id}). HTTP Status: {response.status_code}")
                    return
                
                # Parse JSON response
                player_data = response.json()

                # only obtains regular season data, excludes preseason
                avgs = player_data["seasonTypes"][0]["summary"]["stats"][0]["stats"]
                
                 # Match player by name
                player_obj = Player.objects.filter(name=name, team=team_obj).first()
                
                if player_obj:
                    # update Player object data
                    self.stdout.write(f"Updating {name}'s data...")
                    player_obj.minutes_per_game = avgs[0]
                    player_obj.points_per_game = avgs[13]
                    player_obj.assists_per_game = avgs[8]
                    player_obj.rebounds_per_game = avgs[7]
                    player_obj.three_pointers_per_game = avgs[3]
                    player_obj.steals_per_game = avgs[10]
                    player_obj.blocks_per_game = avgs[9]
                    player_obj.turnovers_per_game = avgs[12]
                    player_obj.fouls_per_game = avgs[11]
                    player_obj.save()
                else:
                    # create new Player object
                    self.stdout.write(f"Creating player data for {name}...")
                    new_player_obj = Player(
                        name = name,
                        team = team_obj,
                        position = pos,
                        minutes_per_game = avgs[0],
                        points_per_game = avgs[13],
                        assists_per_game = avgs[8],
                        rebounds_per_game = avgs[7],
                        three_pointers_per_game = avgs[3],
                        steals_per_game = avgs[10],
                        blocks_per_game = avgs[9],
                        turnovers_per_game = avgs[12],
                        fouls_per_game = avgs[11]
                    )
                    new_player_obj.save() #save to the database
                self.stdout.write(f"Data for {name} successfully updated.")
                
                # logic for player gamelogs
                player_gamelogs = [] #store player gamelogs e.g. [opponent, date]
                for event in player_data["events"].values():
                    date_str = event["gameDate"].split("T")[0] #YYYY-MM-DD format
                    # Default to "N/A" if 'abbreviation' is missing/certain preseason games played against non-NBA teams
                    abbreviation = event["opponent"].get("abbreviation", "N/A")  # Default to "N/A" if 'abbreviation' is missing
                    player_gamelogs.append([abbreviation, date_str])

                # ESPN API already lists games in chronological order so no need to match ids
                gamelogs = player_data["seasonTypes"][0]["categories"]
                player_obj_name = Player.objects.get(name=name)
                count = 0
                for month in gamelogs:
                    for game in month["events"]:
                        # create PlayerGameLog object
                        player_game_log_obj = PlayerGameLog(
                            player = player_obj_name,
                            date = player_gamelogs[count][1],
                            opponent = player_gamelogs[count][0],
                            minutes = game["stats"][0],
                            points = game["stats"][13],
                            assists = game["stats"][8],
                            rebounds = game["stats"][7],
                            three_pointers = game["stats"][3],
                            steals = game["stats"][10],
                            blocks = game["stats"][9],
                            turnovers = game["stats"][12],
                            fouls = game["stats"][11]
                        )
                        count += 1
                        player_game_log_obj.save() #save player gamelog to the database
                self.stdout.write(f"Gamelogs for {name} successfully updated.")
        except requests.exceptions.RequestException as e:
            self.stdout.write(f"Error updating players: {e}")