from src.accountPersonal import AccountPersonal


class TestAccount:
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
        acc.balance = 100.0
        acc.outgoing_transfer(200.0)
    def test_transfer_out_correct(self):
        acc = AccountPersonal('John','Skyrim','12345678901')
        acc.balance = 300.0
        acc.outgoing_transfer(200.0)