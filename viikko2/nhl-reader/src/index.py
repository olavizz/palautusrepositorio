from rich.console import Console
from rich.table import Table
from player import PlayerReader, PlayerStats

def main():
    season = input("Enter season: [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26] ")
    nationality = input("Enter nationality: [USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/NED/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS] ")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    players = stats.top_scorers_by_nationality(nationality)

    table = Table(title=f"Season {season} players from {nationality}")

    table.add_column("Name", justify="center", style="bright_magenta")
    table.add_column("Teams", justify="center", style="light_sea_green")
    table.add_column("Goals", justify="center", style="orange_red1")
    table.add_column("Assists", justify="center", style="chartreuse1")
    table.add_column("Points", justify="center", style="dark_slate_gray2")

    for player in players:
        table.add_row(f"{player.name}", f"{player.team}", f"{player.goals}", f"{player.assists}", f"{player.points}")

    console = Console()
    console.print(table)

if __name__ == "__main__":
    main()
