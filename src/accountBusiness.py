import os
import requests
from datetime import date
from src.smtp.smtp import SMTPClient
from src.account import Account

class AccountBusiness(Account):
    def __init__(self,company_name,nip):
        self.company_name = company_name
        self.balance = 0.0
        self.fee = 5.0  
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        if self.nip != "Invalid":
            if not self.validate_nip_with_mf(self.nip):
                raise ValueError("Company not registered")
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
    
    def validate_nip_with_mf(self, nip):
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().strftime("%Y-%m-%d")
        url = f"{base_url}/api/search/nip/{nip}?date={today}"

        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            print("MF API response:", response.text)

            if response.status_code == 200:
                data = response.json()
                subject = data.get("result", {}).get("subject")
                if subject and subject.get("statusVat") == "Czynny":
                    return True
        except Exception as e:
            print("Error contacting MF API:", e)

        return False
    
    def send_history_via_email(self, email_address: str) -> bool:
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        text = f"Company account history: {self.history}"

        return SMTPClient.send(subject, text, email_address)