from kps import KiviPaperiSakset
from tekoaly import Tekoaly


class KPSTekoaly(KiviPaperiSakset):
    def __init__(self):
        self._tekoaly = Tekoaly()

    def _hae_siirrot(self):
        ekan_siirto = input("Ensimmäisen pelaajan siirto: ")
        tokan_siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")
        return ekan_siirto, tokan_siirto
