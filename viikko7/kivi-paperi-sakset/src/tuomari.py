# Luokka pitää kirjaa ensimmäisen ja toisen pelaajan pisteistä sekä tasapelien määrästä.
# Lisätty logiikka, jolla voidaan tarkistaa, onko jollain pelaajalla voittaja (5 voittoa).
class Tuomari:
    def __init__(self):
        self.ekan_pisteet = 0
        self.tokan_pisteet = 0
        self.tasapelit = 0
        # Sisäinen kenttä tallentamaan voittajan tila kun jompikumpi saavuttaa 5 voittoa
        # Arvo voi olla "eka", "toka" tai None
        self._voittaja = None

    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        if self._tasapeli(ekan_siirto, tokan_siirto):
            self.tasapelit = self.tasapelit + 1
        elif self._eka_voittaa(ekan_siirto, tokan_siirto):
            self.ekan_pisteet = self.ekan_pisteet + 1
        else:
            self.tokan_pisteet = self.tokan_pisteet + 1

        # Päivitetään voittajatila jos jollain on nyt 5 tai enemmän voittoja
        if self.ekan_pisteet >= 3:
            self._voittaja = "eka"
        elif self.tokan_pisteet >= 3:
            self._voittaja = "toka"

    def __str__(self):
        base = f"Pelitilanne: {self.ekan_pisteet} - {self.tokan_pisteet}\nTasapelit: {self.tasapelit}"
        if self._voittaja is not None:
            if self._voittaja == "eka":
                winner_text = "Ensimmäinen pelaaja voitti pelin!"
            else:
                winner_text = "Toinen pelaaja voitti pelin!"
            return base + "\n" + winner_text
        return base

    def onko_voittaja(self):
        """Palauttaa True jos jompikumpi pelaajista on saavuttanut 5 voittoa."""
        return self._voittaja is not None

    def voittaja(self):
        """Palauttaa 'eka' jos ensimmäinen pelaaja voitti, 'toka' jos toinen voitti, muuten None."""
        return self._voittaja

    # sisäinen metodi, jolla tarkastetaan tuliko tasapeli
    def _tasapeli(self, eka, toka):
        if eka == toka:
            return True

        return False

    # sisäinen metodi joka tarkastaa voittaako eka pelaaja tokan
    def _eka_voittaa(self, eka, toka):
        if eka == "k" and toka == "s":
            return True
        elif eka == "s" and toka == "p":
            return True
        elif eka == "p" and toka == "k":
            return True

        return False
