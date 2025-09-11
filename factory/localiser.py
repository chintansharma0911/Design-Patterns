from abc import ABC, abstractmethod


class Localiser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def localise(self, msg):
        pass
