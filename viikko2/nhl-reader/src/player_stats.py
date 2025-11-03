from player_reader import PlayerReader

class PlayerStats:
    def __init__(self, PlayerR):
        self.playerfunc = PlayerR

    def top_scorers_by_nationality(self, nationality):
        players = self.playerfunc.get_players()

        players_by_nationality = list(filter(lambda x: x.nationality == nationality, players))

        players_by_nationality.sort(key=lambda player: player.points, reverse= True)

        return players_by_nationality
    
