import requests 
import json
from ..db.models import Player, Team
from ..db import db_session
from urllib.parse import urlencode

class OctaneApi: 
    def __init__(self):
        self.url = "https://zsr.octane.gg/"
    
    def get(self,uri):
        return json.loads(requests.get(uri).response)

    def get_teams(self,active=False):
        url = self.url + f'/teams{"/active" if active else ""}'
        return self.get(url)
    

    def get_player_stats(self,**kwargs):
        uri = self.url + "/players/" + urlencode(kwargs)
        return self.get(uri)


    






        

    




