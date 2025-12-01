class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.m_score1 += 1
        else:
            self.m_score2 += 1

    def get_score(self):
        if self.m_score1 == self.m_score2:
            score = self.even_score()

        elif self.m_score1 >= 4 or self.m_score2 >= 4:
            score = self.advantage_scoring()
        else:
            score = self.normal_score()
        return score

    def even_score(self):
        if self.m_score1 > 2:
            return "Deuce"
        calls = ["Love-All", "Fifteen-All", "Thirty-All"]
        return calls[self.m_score1]

    def advantage_scoring(self):
        game_score = self.m_score1 - self.m_score2

        if game_score == 1:
            score = "Advantage player1"
        elif game_score == -1:
            score = "Advantage player2"
        elif game_score >= 2:
            score = "Win for player1"
        else:
            score = "Win for player2"
        return score

    def normal_score(self):
        calls = ["Love", "Fifteen", "Thirty", "Forty"]
        score = calls[self.m_score1]
        score += f"-{calls[self.m_score2]}"
        return score
