from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe",'12345678910')
        assert account.balance == 0.0
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == '12345678910'
    
    def test_invalid_pesel_short(self):
        account = Account("Jane", "Doe",'1234510')
        assert account.pesel == "Invalid"
    
    def test_invalid_pesel_long(self):
        account = Account("Jane", "Doe",'1234510123142141421312','XY')
        assert account.pesel == "Invalid"
    
    def test_None_pesel(self):
        account = Account("Jane", "Doe", None,'XY')
        assert account.pesel == "Invalid"
    
    def test_no_promo_code(self):
        acc = Account("John", "Doe",'12345678910')
        assert acc.balance == 0
    
    def test_with_promo_code(self):
        acc = Account('Joh',"Does",'123456789011','XYZ')
        assert acc.balance == 50
    
    def test_with_wrong_promo_code(self):
        acc = Account('Joh',"Does",'123456789011','XY')
        assert acc.balance == 0
    
    def test_with_code_wrong_age(self):
        acc = Account('Joh',"Does",'32345678901','XYZ')
        assert acc.balance == 0
    
    def test_with_code_correct_age_2000(self):
        acc = Account('Joh',"Does",'22345678901','XYZ')
        assert acc.balance == 50
    
    def test_with_code_correct_age_2000(self):
        acc = Account('Joh',"Does",'92345678901','XYZ')
        assert acc.balance == 50