from src.account import Account

class AccountBusiness(Account):
    def __init__(self,company_name,nip):
        self.company_name = company_name
        self.balance = 0.0
        self.fee = 5.0  
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.history = []
    
    def is_nip_valid(self,nip):
        if isinstance(nip,str) and len(nip) == 10:
            return True
        return False
    
    def take_loan(self,amount):
        def not_valid_for_loan(self):
            hist = self.history
            #saldo na rachunku (balance) musi być co najmniej 2 razy większe niż kwota zaciąganego kredytu (amount),
            def wrong_balance():
                if self.balance <= 2*amount:
                    return True
                return False
            #w historii znajduje się przynajmniej jeden przelew wychodzący o kwocie dokładnie 1775
            def zus():
                if -1775.0 not in hist:
                    return True
                return False
            #konto musi mieć co najmniej pięć transakcji
            if wrong_balance() or zus():
                return True
            else:
                return False

        if not_valid_for_loan(self):
            return False
        else:
            self.balance += amount
            self.history.append(amount)
            return True
