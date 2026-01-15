from src.accountPersonal import AccountPersonal

class AccountRegistry:
    def __init__(self):
        self.accounts = []
    
    def add_account(self, account: AccountPersonal):
        self.accounts.append(account)
        return
    
    def search_account(self, id_pesel):
        for acc in self.accounts:
            if acc.pesel == str(id_pesel):
                return acc
        return None
    
    def return_all_accs(self):
        return self.accounts
        