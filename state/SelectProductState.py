from state.DispensingState import DispensingState
from state.states import State


class SelectProductState(State):
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
        inventory = machine.getInventory()
        if inventory.get(productCode):
            coinlist = machine.getCoins()
            total =0
            for i in coinlist:
                total +=i
            price = inventory.get(productCode).get('price')
            if total >= price:
                self.getChange(machine, total - price)
                machine.setState(DispensingState())
        else:
            print('Cannot do this operation')
        return

    def dispenseProduct(self, machine):
        print('Cannot do this operation')
        return

    def refundFullMoney(self, machine):
        print('Cannot do this operation')
        return

    def getChange(self, machine, money):
        print('Dispensing extraaa changeee of' + str(money))
        machine.setCoins([])
        return
