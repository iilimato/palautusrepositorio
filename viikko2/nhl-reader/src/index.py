from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from player_reader import PlayerReader
from player_stats import PlayerStats


def main():
    season_input = kysy_kausi()
    nationality = kysy_kansallisuus()
    players = hae_pelaajat(season_input, nationality)
    nayta_pelaajat(season_input, nationality, players)


def kysy_kausi():
    console = Console()
    seasons = ["2018-19", "2019-20", "2020-21", "2021-22",
               "2022-23", "2023-24", "2024-25", "2025-26"]
    console.print(
        f"\nSeason [magenta][{'/'.join(seasons)}][/magenta] "
        f"([magenta]2024-25[/magenta]):",
        style="bold"
    )
    return Prompt.ask("", default="2024-25")


def kysy_kansallisuus():
    console = Console()
    nationalities = ["USA", "FIN", "CAN", "SWE", "CZE", "RUS",
                     "SLO", "FRA", "GBR", "SVK", "DEN", "NED",
                     "AUT", "BLR", "GER", "SUI", "NOR", "UZB",
                     "LAT", "AUS"]
    console.print(
        f"\nNationality [magenta][{'/'.join(nationalities)}][/magenta] ():",
        style="bold"
    )
    return Prompt.ask("").upper()


def hae_pelaajat(season_input, nationality):
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season_input}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    return stats.top_scorers_by_nationality(nationality)


def nayta_pelaajat(season_input, nationality, players):
    console = Console()
    console.print(
        f"\n[italic]Season {season_input} "
        f"players from {nationality}[/italic]\n"
    )

    table = luo_taulukko()
    tayta_taulukko(table, players)

    console.print(table)
    console.print()


def luo_taulukko():
    table = Table(show_header=True, header_style="bold")
    table.add_column("Released", style="cyan")
    table.add_column("teams", style="magenta")
    table.add_column("goals", justify="right", style="green")
    table.add_column("assists", justify="right", style="green")
    table.add_column("points", justify="right", style="green")
    return table


def tayta_taulukko(table, players):
    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists))


if __name__ == "__main__":
    main()
