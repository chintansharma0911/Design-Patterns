from state.HasMoneyState import HasMoneyState
from state.states import State


class IdleState(State):
    def clickOnInsertCoinButton(self, machine):
        print('Starting Transaction------ ')
        print('Turning on the vending machine')
        machine.setState(HasMoneyState())
        pass

    def clickOnStartProductSelection(self, machine):
        print('Cannot do this operation')
        return

    def insertCoin(self, machine, coin):
        print('Cannot do this operation')
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