class TennisGame:
    # Tennis score constants
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
    
    def score_name(self, score):
        """Palauttaa pistemäärää vastaavan nimen."""
        score_names = {
            self.love: "Love",
            self.fifteen: "Fifteen",
            self.thirty: "Thirty",
            self.forty: "Forty"
        }
        return score_names[score]
    
    def get_score(self):
        score = ""
        temp_score = 0
        
        if self.player1_score == self.player2_score:
            if self.player1_score == self.love:
                score = "Love-All"
            elif self.player1_score == self.fifteen:
                score = "Fifteen-All"
            elif self.player1_score == self.thirty:
                score = "Thirty-All"
            else:
                score = "Deuce"
        elif self.player1_score >= self.win_threshold or self.player2_score >= self.win_threshold:
            minus_result = self.player1_score - self.player2_score
            
            if minus_result == 1:
                score = "Advantage player1"
            elif minus_result == -1:
                score = "Advantage player2"
            elif minus_result >= self.win_margin:
                score = "Win for player1"
            else:
                score = "Win for player2"
        else:
            for i in range(1, 3):
                if i == 1:
                    temp_score = self.player1_score
                else:
                    score = score + "-"
                    temp_score = self.player2_score
                
                score = score + self.score_name(temp_score)
        
        return score