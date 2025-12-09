class Summa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = 0

    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.plus(self._lue_syote())

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = 0

    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.miinus(self._lue_syote())

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = 0

    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Kumoa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote

    def suorita(self):
        pass


class Komentotehdas:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote

    def hae(self, komento):
        komennot = {
            "SUMMA": Summa(self._sovelluslogiikka, self._lue_syote),
            "EROTUS": Erotus(self._sovelluslogiikka, self._lue_syote),
            "NOLLAUS": Nollaus(self._sovelluslogiikka, self._lue_syote),
            "KUMOA": Kumoa(self._sovelluslogiikka, self._lue_syote)
        }

        return komennot.get(komento.name, Kumoa(self._sovelluslogiikka, self._lue_syote))
