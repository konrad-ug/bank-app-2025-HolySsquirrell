from src.account import AccountPersonal

class AccountPersonal(AccountPersonal):
    def __init__(self, first_name, last_name, pesel, code = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0 if (self.valid_code(code) or self.is_old_enough(pesel)) else 50.0 
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
    
    def is_pesel_valid(self,pesel):
        if isinstance(pesel,str) and len(pesel) == 11:
            return True
        return False
    def valid_code(self, code):
        if isinstance(code,str) and len(code) == 3: 
            return False
        return True 
    def is_old_enough(self,pesel):
        peselInt = int(pesel)
        if (peselInt > 60999999999 or peselInt < 25000000000):
            return False
        return True
