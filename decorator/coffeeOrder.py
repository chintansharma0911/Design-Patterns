from abc import ABC, abstractmethod

class Coffee(ABC):

    @abstractmethod
    def get_desc(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass


class Decaf(Coffee):
    def get_desc(self):
        return 'Decaf '

    def get_cost(self):
        return 10

class Espresso(Coffee):
    def get_desc(self):
        return 'Espresso '

    def get_cost(self):
        return 20


class CoffeeDecorator(Coffee):
    @abstractmethod
    def get_cost(self):
        pass
    @abstractmethod
    def get_desc(self):
        pass


class WhippedMilk(CoffeeDecorator):

    def __init__(self, coffee):
        self.coffee = coffee

    def get_desc(self):
        return 'WhippedMilk ' + self.coffee.get_desc()

    def get_cost(self):
        return self.coffee.get_cost() + 10


class Caramel(CoffeeDecorator):

    def __init__(self, coffee):
        self.coffee = coffee

    def get_desc(self):
        return 'Caramel '+self.coffee.get_desc()

    def get_cost(self):
        return self.coffee.get_cost() + 60