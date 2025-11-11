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


if __name__ == '__main__':

    vendingMachine = Machine()
    vendingMachine.setInventory(
        {'101': {'price': 100},
         '102': {'price': 300},
         '103': {'price': 200}
         }
    )


    currentState = vendingMachine.getState()
    currentState.clickOnInsertCoinButton(vendingMachine)


    currentState = vendingMachine.getState()
    currentState.insertCoin(vendingMachine, [50,60,122])

    currentState.clickOnStartProductSelection(vendingMachine)

    currentState = vendingMachine.getState()
    currentState.chooseProduct(vendingMachine, '101')


    currentState = vendingMachine.getState()
    currentState.dispenseProduct(vendingMachine, '101')

    print(vendingMachine.getInventory())
    print(vendingMachine.getState())