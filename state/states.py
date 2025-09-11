from abc import abstractmethod, ABC


class State(ABC):
    @abstractmethod
    def clickOnInsertCoinButton(self, machine):
        pass

    @abstractmethod
    def clickOnStartProductSelection(self, machine):
        pass

    @abstractmethod
    def insertCoin(self, machine, coin):
        pass

    @abstractmethod
    def chooseProduct(self, machine, productCode):
        pass

    @abstractmethod
    def dispenseProduct(self, machine):
        pass

    @abstractmethod
    def refundFullMoney(self, machine):
        pass

    @abstractmethod
    def getChange(self, machine, money):
        pass
