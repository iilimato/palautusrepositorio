from kps import KiviPaperiSakset
from tekoaly_parannettu import TekoalyParannettu


class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__(self):
        self._tekoaly = TekoalyParannettu(10)

    def _hae_siirrot(self):
        ekan_siirto = input("Ensimmäisen pelaajan siirto: ")
        tokan_siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")
        self._tekoaly.aseta_siirto(ekan_siirto)
        return ekan_siirto, tokan_siirto
