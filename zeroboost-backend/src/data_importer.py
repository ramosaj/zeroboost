
from db.models import Player, Team, Games, ScoreboardStats
from db import db_session
from .octane_wrapper import OctaneApi
from .replay_aggregator import ReplayAggregator

class DataImporter: 
    def __init__(self):
        self.api = OctaneApi()

    def db_insert(self,object):
        db_session.add(object)
        db_session.commit()

    def import_all_teams(self,active=False):
        resp_dict = self.api.get_all_teams(active=active)
        for team in resp_dict['teams']: 
            team_i = team['team'] if active else team
            team_object = Team(
                octane_id = team_i.get('_id'),
                name = team_i.get('name'),
                region = team_i.get('region'),
                image = team_i.get('image'), 
            )
            
            if (len(Team.query.where(Team.octane_id == team_i['_id']).all()) == 0):
                print(f'Importing {team_i["name"] }')
                self.db_insert(team_object)

            if active: 
                for player in team['players']:
                    accounts = player.get('accounts')
                    platform = accounts[0]['platform'] if accounts else None
                    id = accounts[0]['id'] if accounts else None
                    ballchasing_id = f'{platform}:{id}' if platform and id else None
                    player_object = Player( 
                        octane_id = player.get('_id'),
                        team_id = team_object.id,
                        ballchasing_id = ballchasing_id,
                        name = player.get('tag'),
                        active= True,
                    )
    
                    if(len(Player.query.where(Player.octane_id == player['_id']).all()) == 0):
                        print(f'Importing {player["tag"]}')
                        self.db_insert(player_object)

    def import_players(self):
        teams = Team.query.all()
        for team in teams:
            team_json = api.get_players(team=team.octane_id)
            for player in team_json['players']:
                id = player['id']
                platform = player['platform']
                ballchasing_id = f'{platform}:{id}'
                octane_id = player['_id']
                player_object = Player(
                    octane_id = octane_id, 
                    ballchasing_id = ballchasing_id,
                    team_id = team_object.id,
                )

                self.db_insert(player_object)
    def import_games_and_scoreboard_stats(self):
        ## get players 
        teams = Team.query.all()
        for team in teams: 
            request = self.api.get_games(team=team.octane_id)
            for game in request['games']:
                blue = game['blue']
                orange = game['orange']
                orange_team = Team.query.filter(Team.octane_id == orange['team']['team']['_id']).first()
                if orange_team is None: 
                    orange_team = self.add_team(
                        octane_id = orange['team']['team']['_id'],
                        name = orange['team']['team']['name'],
                        image = orange['team']['team']['image'] if 'image' in orange['team']['team'] else None,
                        )
                blue_team = Team.query.filter(Team.octane_id == blue['team']['team']['_id']).first()
                if blue_team is None: 
                    blue_team = self.add_team(
                        octane_id = blue['team']['team']['_id'],
                        name = blue['team']['team']['name'],
                        image = blue['team']['team']['image'] if 'image' in blue['team']['team'] else None
                        )
                print(f'Importing {blue_team.name} vs {orange_team.name}')
                game_object = Games.query.filter(Games.octane_id == game['_id']).first()

                if game_object is None: 
                    game_object = Games(
                        title = game['match']['event']['name'],
                        date = game['date'],
                        duration = game['duration'],
                        octane_id = game['_id'],
                        team_1 = blue_team.id,
                        team_2 = orange_team.id,
                        is_professional = True,
                        game_in_series = game['number']
                    )
                    self.db_insert(game_object)

                for player in blue['players']:
                    self.parse_player(player,blue_team.id,game_object)
                
                for player in orange['players']:
                    self.parse_player(player,orange_team.id,game_object)

                    
    def parse_player(self,player,team,game_object):
        team_player = Player.query.filter(Player.octane_id == player['player']['_id']).first()
        if team_player is None: 
            team_player = self.add_player(
                name = player['player']['tag'],
                octane_id = player['player']['_id'],
                team = team
                )
        
        stats_for_game = ScoreboardStats.query.join(Player).join(Games).filter(Player.id == team_player.id, Games.id == game_object.id).first() 
        if stats_for_game is not None:
            print(f'Skipped {team_player.name} in {game_object.title}')
            return
        core_stats = player['stats']['core']
        
        scoreboard_stat = ScoreboardStats(
            player_id = team_player.id,
            game_id = game_object.id,
            goals = core_stats['goals'],
            shots = core_stats['shots'],
            assists = core_stats['assists'],
            saves = core_stats['saves'],
            score = core_stats['score'],
            demolitions = player['stats']['demo']['inflicted'],
        )
        self.db_insert(scoreboard_stat)

    def add_team(self,octane_id, name, image,region=None):
        print(f"Unknown Team Found {name}")
        team = Team( 
            octane_id = octane_id, 
            name = name, 
            image = image, 
            region = region,
        )
        self.db_insert(team)

        return team
    def add_player(self,team, name, octane_id, active=True):
        print(f"Unknown Player Found {name}")
        player = Player(
            name = name, 
            octane_id = octane_id, 
            active = active,
            team_id = team,
        )
        self.db_insert(player)
        return player


