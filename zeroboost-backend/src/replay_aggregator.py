import ballchasing
import os
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta

class ReplayAggregator:

    def __init__(self, platform, player_id):
        self.api = ballchasing.Api(os.getenv('BALLCHASING_API_TOKEN'))
        self.platform = platform
        self.player_id = player_id 
    

    def get_replays(self,count=10,n_months=5):
        replay_list = []
        
        dates = self.build_date_range(start=dt.datetime.today()-relativedelta(months=n_months))
        print(dates)
        monthly_replays = []
        for i in range(1,len(dates)):
            replays = self.api.get_replays(replay_after=dates[i-1],replay_before=dates[i],player_id=f'{self.platform}:{self.player_id}',count=count)
            monthly_replays += list(replays)

        for replay in monthly_replays:
            replay_list.append(self.parse_replay(replay['id']))
        
        replay_df = pd.DataFrame(replay_list)
        replay_df['year'] = pd.to_datetime(replay_df['date'],utc=True).dt.year
        replay_df['month'] = pd.to_datetime(replay_df['date'],utc=True).dt.month
        replay_grouped_by_month = replay_df.groupby([replay_df['year'], replay_df['month']]).mean().reset_index()

        
        return { 
            'bpm': replay_grouped_by_month[['month',"year",'bpm']].to_dict('records')  ,
            'shooting_percentage': replay_grouped_by_month[["month","year",'shooting_percentage']].to_dict('records'),
        }

    
    def build_date_range(self,start=dt.datetime.today()-relativedelta(months=1),end=dt.datetime.today()):

        return pd.date_range(start=start,end=end,freq='M').to_series().apply(lambda x: x.isoformat("T") + 'Z').values
    

    def get_replay_by_date(self, frequency='W'):
        pass
        


    def parse_replay(self,id):
        replay = self.api.get_replay(id)
        blue_player = list(filter(lambda x: self.find_player(x,self.player_id), replay['blue']['players']))
        orange_player =  list(filter(lambda x: self.find_player(x,self.player_id), replay['orange']['players']))
        
        if len(blue_player) > 0:
            team = 'blue'
            player = blue_player[0]
        else: 
            team = 'orange'
            player = orange_player[0]
        
        return {
            'date': replay['date'], 
            'bpm' : player['stats']['boost']['bpm'],
            'shooting_percentage': player['stats']['core']['shooting_percentage'],
            'goal_participation': self.calculate_goal_participation(replay,player,team)
        }
            
    
    def find_player(self,potential_id,player_id):
        if potential_id['id']['id'] == player_id:
            return True 
        else:
            return False

    def calculate_goal_participation(self,replay, player, team):
        ## Number of goals scored + Number of assists / total team goals
        total_goals = replay[team]['stats']['core']['goals']
        if total_goals == 0 : return 0
        total_goals = (player['stats']['core']['goals'] + player['stats']['core']['assists']) / total_goals
        return total_goals
       

        

       









    
        