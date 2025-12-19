from abc import ABC, abstractmethod

from tuomari import Tuomari


class KiviPaperiSakset(ABC):
    def pelaa(self):
        tuomari = Tuomari()

        ekan_siirto = self._ensimmaisen_siirto()
        tokan_siirto = self._toisen_siirto()

        self._tietokone_viesti(tokan_siirto)

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto = input("Ensimmäisen pelaajan siirto: ")
            tokan_siirto = self._toisen_siirto()
            self._aseta_tkoaly_siirto(tokan_siirto)
            self._tietokone_viesti(tokan_siirto)

        print("Kiitos!")
        print(tuomari)

    def _ensimmaisen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    # tämän metodin toteutus vaihtelee eri pelityypeissä
    @abstractmethod
    def _toisen_siirto(self):
        pass

    def _tietokone_viesti(self, viesti):
        pass

    def _aseta_tkoaly_siirto(self, siirto):
        pass

    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"
