import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []

    print("Players from FIN:")
    print("")

    for player_dict in response:
        player = Player(player_dict)

        if player.nationality == "FIN":
            players.append(player)
        else:
            continue
    
    players.sort(key=lambda player: player.points, reverse= True)

    for player in players:
        print(player)

if __name__ == "__main__":
    main()
