from src.account import AccountPersonal

class AccountBusiness(AccountPersonal):
    def __init__(self,company_name,nip):
        self.company_name = company_name
        self.balance = 0.0
        self.fee = 5.0  
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
    
    def is_nip_valid(self,nip):
        if isinstance(nip,str) and len(nip) == 10:
            return True
        return False
