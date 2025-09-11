from abc import ABC, abstractmethod


class Colleague(ABC):
    @abstractmethod
    def bid(self, amount, auction):
        pass

    @abstractmethod
    def notifybid(self, amount, auctionName):
        pass


class Bidder(Colleague):
    def __init__(self, name):
        self.name = name

    def bid(self, amount, auction):
        auction.receiveBid(amount, self)

    def notifybid(self, amount, auctionName):
        print(f"Hey {self.name}, current bid is {amount} for {auctionName}")


class Auction(ABC):
    @abstractmethod
    def receiveBid(self, amount, bidder):
        pass

    @abstractmethod
    def addBidder(self, bidder):
        pass


class AuctionMediator(Auction):
    def __init__(self, name):
        self.bidders = []
        self.name = name
        self.currentBidAmount = 0
        self.currentBidder = None

    def addBidder(self, bidder):
        self.bidders.append(bidder)

    def receiveBid(self, amount, bidder):
        if bidder not in self.bidders:
            print(f"{bidder.name} is not registered for {self.name}")
            return

        if amount > self.currentBidAmount:
            self.currentBidAmount = amount
            self.currentBidder = bidder
            for each in self.bidders:
                if each != bidder:
                    each.notifybid(amount, self.name)
        else:
            print(f"Bid of {amount} is too low! Current highest bid is {self.currentBidAmount}.")
