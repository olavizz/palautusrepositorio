from player import Player
import requests

class PlayerReader:
    def __init__(self, url):
        self.url = url
        self.players = []
    
    def get_players(self):
        response = requests.get(self.url).json()
        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)
        return self.players
