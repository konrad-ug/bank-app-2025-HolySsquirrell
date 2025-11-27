from src.accountPersonal import AccountPersonal
import pytest

class TestAccount:
    @pytest.fixture(autouse=True, scope="function")
    def account(self):
        self.account = AccountPersonal('Joh',"Does",'22345678901','XYZ')

    def test_account_creation(self):
        account = AccountPersonal("John", "Doe",'12345678910')
        assert account.balance == 0.0
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == '12345678910'
    
    def test_invalid_pesel_short(self):
        account = AccountPersonal("Jane", "Doe",'1234510')
        assert account.pesel == "Invalid"
    
    def test_invalid_pesel_long(self):
        account = AccountPersonal("Jane", "Doe",'1234510123142141421312','XY')
        assert account.pesel == "Invalid"
    
    def test_None_pesel(self):
        account = AccountPersonal("Jane", "Doe", None,'XY')
        assert account.pesel == "Invalid"
    
    def test_no_promo_code(self):
        acc = AccountPersonal("John", "Doe",'12345678910')
        assert acc.balance == 0
    
    def test_with_promo_code(self):
        acc = AccountPersonal('Joh',"Does",'123456789011','XYZ')
        assert acc.balance == 50
    
    def test_with_wrong_promo_code(self):
        acc = AccountPersonal('Joh',"Does",'123456789011','XY')
        assert acc.balance == 0
    
    def test_with_code_wrong_age(self):
        acc = AccountPersonal('Joh',"Does",'32345678901','XYZ')
        assert acc.balance == 0
    
    def test_with_code_correct_age_2000(self):
        acc = AccountPersonal('Joh',"Does",'22345678901','XYZ')
        assert acc.balance == 50
    
    def test_with_code_correct_age_2000(self):
        acc = AccountPersonal('Joh',"Does",'92345678901','XYZ')
        assert acc.balance == 50
        
    def test_transfer_out_wrong(self):
        acc = AccountPersonal('John','Skyrim','12345678901')
        self.account.balance = 100.0
        self.account.outgoing_transfer(200.0)
        assert self.account.balance == 100.0
        assert self.account.history == []

    def test_transfer_out_correct(self):
        self.account.balance = 300.0
        self.account.outgoing_transfer(200.0)
        assert self.account.balance == 100.0
        assert self.account.history == [-200.0]

    def test_transfer_out_express_correct_with_negative_balance_end(self):
        self.account.balance = 300.0
        self.account.outgoing_transfer_express(300.0)
        assert self.account.balance == -1.0
        assert self.account.history == [-300.0,-1.0]

    def test_transfer_out_express_wrong(self):
        self.account.balance = 300.0
        self.account.outgoing_transfer_express(400.0)
        assert self.account.balance == 300.0
        assert self.account.history == []
    
    def test_loan_correct(self):
        self.account.balance = 500.0
        self.account.history = []
    
    