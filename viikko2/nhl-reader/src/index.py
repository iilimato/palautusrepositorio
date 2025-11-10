import requests
from player import Player
from player_reader import PlayerReader
from player_stats import PlayerStats

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

def main():
    console = Console()

    seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    console.print(f"\nSeason [magenta][{'/'.join(seasons)}][/magenta] ([magenta]2024-25[/magenta]):", style="bold")
    
    season_input = Prompt.ask("", default="2024-25")

    nationalities = ["USA", "FIN", "CAN", "SWE", "CZE", "RUS", "SLO", "FRA", "GBR", "SVK", "DEN", "NED", "AUT", "BLR", "GER", "SUI", "NOR", "UZB", "LAT", "AUS"]
    console.print(f"\nNationality [magenta][{'/'.join(nationalities)}][/magenta] ():", style="bold")
    
    nationality = Prompt.ask("").upper()

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season_input}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    console.print(f"\n[italic]Season {season_input} players from {nationality}[/italic]\n")
    
    table = Table(show_header=True, header_style="bold")
    table.add_column("Released", style="cyan")
    table.add_column("teams", style="magenta")
    table.add_column("goals", justify="right", style="green")
    table.add_column("assists", justify="right", style="green")
    table.add_column("points", justify="right", style="green")
    
    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists)
        )
    
    console.print(table)
    console.print()


    #response = requests.get(url).json()

    #print("JSON-muotoinen vastaus:")
    #print(response)

    #players = []

    #for player_dict in response:
    #    player = Player(player_dict)
    #    players.append(player)

    #suomalaiset = []

    #for player in players:
    #    if player.nationality == "FIN":
    #        suomalaiset.append(player)

    #print("Suomalaiset pelaajat:")

    #jarjestetyt = sorted(suomalaiset, key=lambda player: player.goals + player.assists, reverse=True)

    #reader = PlayerReader(url)
    #stats = PlayerStats(reader)
    #players = stats.top_scorers_by_nationality("FIN")

    #for player in players:
    #    print(player)

    #for player in players:
        #print(player)

if __name__ == "__main__":
    main()
