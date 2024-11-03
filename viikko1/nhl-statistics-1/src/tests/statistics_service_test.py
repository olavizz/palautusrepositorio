import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_player_search_successful(self):
        searched_player = self.stats.search("Kurri")
        self.assertEqual(searched_player.name, "Kurri")

    def test_player_search_unsuccessful(self):
        searched_player = self.stats.search("Laine")
        self.assertEqual(searched_player, None)
    
    def test_team_filter(self):
        team = self.stats.team("EDM")
        self.assertEqual(len(team), 3)
    
    def test_top_points(self):
        result = self.stats.top(3)
        print(result)
        for a in result:
            print(a.points)
        for i in range(1, len(result)):
            print(i)
            self.assertGreaterEqual(result[i-1].points, result[i].points)