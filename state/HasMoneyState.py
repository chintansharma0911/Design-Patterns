from state.SelectProductState import SelectProductState
from state.states import State


class HasMoneyState(State):
    def clickOnInsertCoinButton(self, machine):
        print('Cannot do this operation')
        return

    def clickOnStartProductSelection(self, machine):
        print('Changing state to selection of product')
        machine.setState(SelectProductState())
        return

    def insertCoin(self, machine, coin):
        print('Inserting coins')
        machine.setCoins(coin)
        return

    def chooseProduct(self, machine, productCode):
        print('Cannot do this operation')
        return

    def dispenseProduct(self, machine):
        print('Cannot do this operation')
        return

    def refundFullMoney(self, machine):
        print('Cannot do this operation')
        return

    def getChange(self, machine, money):
        print('Cannot do this operation')
        return