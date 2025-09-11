from factory.localiser import Localiser


class EnglishLocaliser(Localiser):
    def __init__(self):
        self.translations = {
            "car": "car",
            "bike": "bike",
            "cycle": "cyclle"
        }

    def localise(self, msg):
        """Translate the message to French."""
        return self.translations.get(msg)