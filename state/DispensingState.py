from state.states import State


class DispensingState(State):

    def clickOnInsertCoinButton(self, machine):
        print('Cannot do this operation')
        return

    def clickOnStartProductSelection(self, machine):
        print('Cannot do this operation')
        return

    def insertCoin(self, machine, coin):
        print('Cannot do this operation')
        return

    def chooseProduct(self, machine, productCode):
        print('Cannot do this operation')
        return

    def dispenseProduct(self, machine, procuctCode):
        inventory = machine.getInventory()
        inventory.pop(procuctCode)
        machine.setInventory(inventory)
        from state.IdleState import IdleState
        machine.setState(IdleState())
        return

    def refundFullMoney(self, machine):
        print('Cannot do this operation')
        return

    def getChange(self, machine, money):
        print('Cannot do this operation')
        return