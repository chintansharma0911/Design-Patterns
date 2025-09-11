from state.IdleState import IdleState


class Machine:
    def __init__(self):
        self.state = IdleState()
        self.inventory = dict
        self.coins = []

    def getState(self):
        return self.state

    def getInventory(self):
        return self.inventory

    def getCoins(self):
        return self.coins

    def setState(self, state):
        self.state = state
        return

    def setInventory(self, inventory):
        self.inventory = inventory
        return

    def setCoins(self, coins):
        self.coins= coins
        return
