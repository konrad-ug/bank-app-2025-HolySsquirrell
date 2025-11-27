class AccountPersonal:
    

    def outgoing_transfer(self,amount):
        if (amount > self.balance or amount < 0):
            return
        else:
            self.balance -= amount
            self.history.append(-amount)
            return
    def outgoing_transfer_express(self,amount):
        if (amount > self.balance or amount < 0):
            return
        else:
            self.balance -= amount
            self.history.append(-amount)
            
            self.balance -= self.fee
            self.history.append(-self.fee)
            return

