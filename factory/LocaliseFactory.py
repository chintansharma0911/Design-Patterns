from abc import ABC, abstractmethod

from factory.localiser import Localiser


class CreateLocaliser(ABC):

    @abstractmethod
    def createLocaliser(self):
        return Localiser
