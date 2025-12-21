from tuomari import Tuomari

# ehkäistään circular import ongelmat


class KiviPaperiSakset:
    @staticmethod
    def luo_peli(pelityyppi):
        from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
        from kps_tekoaly import KPSTekoaly
        from kps_parempi_tekoaly import KPSParempiTekoaly

        if pelityyppi == "a":
            return KPSPelaajaVsPelaaja()
        elif pelityyppi == "b":
            return KPSTekoaly()
        elif pelityyppi == "c":
            return KPSParempiTekoaly()

        return None

    def pelaa(self):
        tuomari = Tuomari()

        ekan_siirto, tokan_siirto = self._hae_siirrot()

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto, tokan_siirto = self._hae_siirrot()

        print("Kiitos!")
        print(tuomari)

    def _hae_siirrot(self):
        raise NotImplementedError("Aliluokan tulee toteuttaa _hae_siirrot")

    def _onko_ok_siirto(self, siirto):
        return siirto in ("k", "p", "s")
