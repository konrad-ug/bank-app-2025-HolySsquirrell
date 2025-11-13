class AccountPersonal:

    def outgoing_transfer(self,amount):
        if (amount > self.balance or amount < 0):
            return
        else:
            self.balance -= amount
            return
