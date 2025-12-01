class TennisGame:
    love = 0
    fifteen = 1
    thirty = 2
    forty = 3
    win_threshold = 4
    win_margin = 2

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score = self.player1_score + 1
        else:
            self.player2_score = self.player2_score + 1

    def _score_name(self, score):
        score_names = {
            self.love: "Love",
            self.fifteen: "Fifteen",
            self.thirty: "Thirty",
            self.forty: "Forty"
        }
        return score_names[score]

    def _format_even_score(self):
        even_score_names = {
            self.love: "Love-All",
            self.fifteen: "Fifteen-All",
            self.thirty: "Thirty-All"
        }

        if self.player1_score in even_score_names:
            return even_score_names[self.player1_score]
        else:
            return "Deuce"

    def _format_advantage_or_win(self):
        score_difference = self.player1_score - self.player2_score

        if score_difference == 1:
            return "Advantage player1"
        elif score_difference == -1:
            return "Advantage player2"
        elif score_difference >= self.win_margin:
            return "Win for player1"
        else:
            return "Win for player2"

    def _format_regular_score(self):
        player1_score_text = self._score_name(self.player1_score)
        player2_score_text = self._score_name(self.player2_score)
        return f"{player1_score_text}-{player2_score_text}"

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self._format_even_score()
        elif self.player1_score >= self.win_threshold or self.player2_score >= self.win_threshold:
            return self._format_advantage_or_win()
        else:
            return self._format_regular_score()
