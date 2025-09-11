from factory.localiser import Localiser


class FrenchLocaliser(Localiser):
    def __init__(self):
        self.translations = {
            "car": "voiture",
            "bike": "bicyclette",
            "cycle": "cyclette"
        }

    def localise(self, msg):
        """Translate the message to French."""
        return self.translations.get(msg)