
from ..db.models import Player, Team
from ..db import db_session
from .octane_wrapper import OctaneApi
from .replay_aggregator import ReplayAggregator

class DataImporter: 
    def __init__():
        self.api = OctaneApi()

    def db_insert(self,object):
        db_session.add(object)
        db_session.commit()

    def import_players_and_teams(self):
        resp_dict = self.api.get_teams()
        for team in resp_dict['teams']: 
            team_object = Team(
                octane_id = team['_id'],
                name = team['team']['name'],
                region = team['team']['region'],
                image = team['team']['name']
            )
            self.db_insert(team_object)
            for player in team['team']['players']:
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
        players = Player.query.all()
        for player in players:  
            request = self.api.get_games(player=player.octane_id)
            for game in request['games']:
                id = game['_id']
                duration = game['duration']
                date = game['date']
                blue = game['blue']
                for players in blue['players']:
                    pass 
                    
                orange = game['orange']