from factory.FrenchLocaliser import FrenchLocaliser
from factory.LocaliseFactory import CreateLocaliser


class FrenchLocaliserFactory(CreateLocaliser):
    def createLocaliser(self):
        return FrenchLocaliser()