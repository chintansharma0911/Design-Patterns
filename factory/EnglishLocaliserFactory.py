from factory.EnglishLocaliser import EnglishLocaliser
from factory.LocaliseFactory import CreateLocaliser


class EnglishLocaliserFactory(CreateLocaliser):
    def createLocaliser(self):
        return EnglishLocaliser()
