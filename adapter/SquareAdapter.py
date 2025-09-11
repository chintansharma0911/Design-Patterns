from abc import ABC, abstractmethod

class Circle(ABC):
    @abstractmethod
    def get_radius(self):
        pass

class RoundCicle(Circle):
    def __init__(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius


class SquarePeg:
    def __init__(self, width):
        self.width = width

    def get_width(self):
        return self.width*8


class SquareAdapter(Circle):

    def __init__(self, squarePeg):
        self._sqpg = squarePeg

    def get_radius(self):
       return self._sqpg.get_width()


