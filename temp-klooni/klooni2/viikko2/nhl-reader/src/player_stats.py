class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        filtered = []
        for player in self.players:
            if player.nationality == nationality:
                filtered.append(player)

        sorted_players = sorted(
            filtered,
            key=lambda player: player.goals + player.assists,
            reverse=True
        )

        return sorted_players

    def toinen_metodi(self):
        pass
