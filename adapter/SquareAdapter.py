from abc import ABC, abstractmethod


#  Class to be adapted to
class Circle(ABC):
    @abstractmethod
    def get_radius(self):
        pass

class RoundCicle(Circle):
    def __init__(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius

# Outlier
class SquarePeg:
    def __init__(self, width):
        self.width = width

    def get_width(self):
        return self.width*8



# Adapter to work as a circle
class SquareAdapter(Circle):

    def __init__(self, squarePeg):
        self._sqpg = squarePeg

    def get_radius(self):
       return self._sqpg.get_width()




# Adapter Method
# from adapter.SquareAdapter import RoundCicle, SquareAdapter, SquarePeg
# circle =RoundCicle(2)
# square = SquarePeg(4)
#
# print(circle.get_radius())
# print(SquareAdapter(square).get_radius())