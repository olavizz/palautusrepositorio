import requests

class Player:
    def __init__(self, dict_):
        self.name = dict_['name']
        self.nationality = dict_['nationality']
        self.team = dict_['team']
        self.goals = dict_['goals']
        self.assists = dict_['assists']
        self.points = dict_['assists'] + dict_['goals']

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {self.points}"

class PlayerReader:
    def __init__(self, url):
        self.url = url
        self.players = []

    def get_players(self):
        response = requests.get(self.url, timeout=10).json()
        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)
        return self.players

class PlayerStats:
    def __init__(self, player_r):
        self.playerfunc = player_r

    def top_scorers_by_nationality(self, nationality):

        players = self.playerfunc.get_players()

        players_by_nationality = list(filter(lambda x: x.nationality == nationality, players))

        players_by_nationality.sort(key=lambda player: player.points, reverse= True)

        return players_by_nationality
