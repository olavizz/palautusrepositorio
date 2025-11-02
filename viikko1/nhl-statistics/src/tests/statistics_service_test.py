import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    
    def test_pelaaja_loytyy_listasta(self):
        pelaaja = self.stats.search("Kurri")

        self.assertEqual(str(pelaaja), "Kurri EDM 37 + 53 = 90")
    
    def test_pelaaja_ei_loydy_listasta(self):
        pelaaja = self.stats.search("Hextall")

        self.assertEqual(pelaaja, None) 
    
    def test_etsii_joukkueen_pelaajat(self):
        pelaajat = self.stats.team("EDM")

        self.assertEqual(str(pelaajat[0]), "Semenko EDM 4 + 12 = 16")
        self.assertEqual(str(pelaajat[1]), "Kurri EDM 37 + 53 = 90")
        self.assertEqual(str(pelaajat[2]), "Gretzky EDM 35 + 89 = 124")
    
    def test_paras_pistemies(self):
        pelaajat = self.stats.top(0, SortBy.POINTS)

        self.assertEqual(str(pelaajat[0]), "Gretzky EDM 35 + 89 = 124")
    
    def test_paras_maalintekija(self):
        pelaajat = self.stats.top(0, SortBy.GOALS)

        self.assertEqual(str(pelaajat[0]), "Lemieux PIT 45 + 54 = 99")
    
    def test_paras_syottaja(self):
        pelaajat = self.stats.top(0, SortBy.ASSISTS)

        self.assertEqual(str(pelaajat[0]), "Gretzky EDM 35 + 89 = 124")
  