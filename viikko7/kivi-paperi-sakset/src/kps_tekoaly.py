from kivi_paperi_sakset import KiviPaperiSakset
from tekoaly import Tekoaly


class KPSTekoaly(KiviPaperiSakset):
    def __init__(self):
        self.tekoaly = Tekoaly()

    def _toisen_siirto(self):
        return self.tekoaly.anna_siirto()

    def _tietokone_viesti(self, viesti):
        print("Tietokone valitsi: ", viesti)
