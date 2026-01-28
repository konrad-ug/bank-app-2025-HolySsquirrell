from src.account import Account
from datetime import date
from src.smtp.smtp import SMTPClient

class AccountPersonal(Account):
    def __init__(self, first_name, last_name, pesel, code = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0 if (self.valid_code(code) or self.is_old_enough(pesel)) else 50.0 
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.fee = 1.0
        self.history = [] 
    
    def is_pesel_valid(self,pesel):
        if isinstance(pesel,str) and len(pesel) == 11:
            return True
        return False
    
    def valid_code(self, code):
        if isinstance(code,str) and len(code) == 8 and code[:5]=="PROM_": 
            return False
        return True 
    
    def is_old_enough(self,pesel):
        peselInt = int(pesel)
        if (peselInt > 60999999999 or peselInt < 25000000000):
            return False
        return True
    

    def submit_for_loan(self,amount):
        def not_valid_for_loan(self):
            hist = self.history
            #Suma ostatnich pięciu transakcji powinna być większa niż kwota wnioskowanego kredytu.
            def suma_5():
                suma = 0
                for i in range(1,6):
                    suma += hist[-i]
                return suma
            #Ostatnie trzy zaksięgowane transakcje powinny być transakcjami wpłaty
            def pos_3():
                if hist[-1] < 0 or hist[-2] < 0 or hist[-3] < 0:
                    return True
                else: 
                    return False
            #konto musi mieć co najmniej pięć transakcji
            if (len(hist) < 5 or suma_5() < amount) or pos_3():
                return True
            else:
                return False

        if not_valid_for_loan(self):
            return 
        else:
            self.balance += amount
            self.history.append(amount)
            return
    
    def send_history_via_email(self, email_address: str) -> bool:
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        text = f"Personal account history: {self.history}"

        return SMTPClient.send(subject, text, email_address)
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.history
        }
        
#1. Ostatnie trzy zaksięgowane transakcje powinny być transakcjami wpłaty, lub
#2. Suma ostatnich pięciu transakcji (konto musi mieć co najmniej pięć transakcji) powinna
#być większa niż kwota wnioskowanego kredytu.
#if (((hist[1]+hist[2]+hist[3]+hist[4]+hist[0]) < amount) or hist[0] < 0 or hist[1] < 0 or hist[2] < 0 or len(hist) < 5)

        
