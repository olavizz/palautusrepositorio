from kivi_paperi_sakset import KiviPaperiSakset
from tekoaly_parannettu import TekoalyParannettu


class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__(self):
        self._tekoaly = TekoalyParannettu(10)

    def _tietokone_viesti(self, tokan_siirto):
        print(f"Tietokone valitsi: {tokan_siirto}")

    def _toisen_siirto(self):
        return self._tekoaly.anna_siirto()

    def _aseta_tkoaly_siirto(self, siirto):
        self._tekoaly.aseta_siirto(siirto)
