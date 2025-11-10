class Player:
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.nationality = player_dict['nationality']
        self.team = player_dict['team']
        self.goals = player_dict['goals']
        self.assists = player_dict['assists']
        self.games = player_dict['games']

    def __str__(self):
        return (f"{self.name:22} {self.team:16}  "
                f"{self.goals:2} + {self.assists:2} = "
                f"{self.goals + self.assists}")
    def toinen_metodi(self):
        pass
