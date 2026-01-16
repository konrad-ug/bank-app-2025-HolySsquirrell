from src.accountPersonal import AccountPersonal
import pytest

class TestAccount:
    @pytest.fixture(autouse=True, scope="function")
    def account(self):
        self.account = AccountPersonal('Joh',"Does",'22345678901','PROM_XYZ')
        self.account.balance = 0

    #---------------------------------------------------------------------------#

    def test_account_creation(self):
        account = AccountPersonal("John", "Doe",'12345678910')
        assert account.balance == 0.0
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == '12345678910'

    #---------------------------------------------------------------------------#

    @pytest.mark.parametrize("Name,Surname,Pesel,Code,expected",
        [
            ("Jane", "Doe",'1234510',None,"Invalid"),
            ("Jane", "Doe",'1234510123142141421312','XY',"Invalid"),
            ("Jane", "Doe", None,'XY',"Invalid")
        ])
    def test_Pesel(self,Name,Surname,Pesel,Code,expected):
        acc = AccountPersonal(Name,Surname,Pesel,Code)
        assert acc.pesel == expected
    
    #---------------------------------------------------------------------------#
    
    @pytest.mark.parametrize("Name,Surname,Pesel,Code,expected",
    [
        ("John", "Doe",'12345678910',None,0),
        ('Joh',"Does",'123456789011','PROM_XYZ',50),
        ('Joh',"Does",'123456789011','XY',0),
        ('Joh',"Does",'32345678901','PROM_XYZ',0),
        ('Joh',"Does",'22345678901','PROM_XYZ',50),
        ('Joh',"Does",'92345678901','PROM_XYZ',50),
        ('Joh',"Does",'92345678901','PRpM_XYZ',0)
    ])
    def test_promo_code(self,Name,Surname,Pesel,Code,expected):
        acc = AccountPersonal(Name,Surname,Pesel,Code)
        assert acc.balance == expected
    
    #---------------------------------------------------------------------------#
    
    @pytest.mark.parametrize("balance,outgoing,expectedB,expectedH",
        [
            (100.0,200.0,100.0,[]),
            (300.0,200.0,100.0,[-200.0])
        ])
    def test_transfer_normal(self,balance,outgoing,expectedB,expectedH):
        self.account.balance = balance
        self.account.outgoing_transfer(outgoing)
        assert self.account.balance == expectedB
        assert self.account.history == expectedH
    
    #---------------------------------------------------------------------------#

    @pytest.mark.parametrize("balance,outgoing,expectedB,expectedH",
        [
            (300.0,300.0,-1.0,[-300.0,-1.0]),
            (300.0,400.0,300.0,[])
        ])
    def test_transfer_express(self,balance,outgoing,expectedB,expectedH):
        self.account.balance = balance
        self.account.outgoing_transfer_express(outgoing)
        assert self.account.balance == expectedB
        assert self.account.history == expectedH

    #---------------------------------------------------------------------------#
    
    @pytest.mark.parametrize("history,loan,expected", 
        [
            ([0.0,200.0,300.0,-150.0,-200.0,-100.0],500.0,0),
            ([0.0,10000.0,300.0,-150.0,-200.0,-100.0],500.0,0),
            ([0.0,10000.0,300.0],500.0,0),
            ([0.0,10000.0,300.0,200.0,100.0],500.0,500.0)
        ])
    def test_loan_tests(self,history,loan,expected):
        self.account.history = history
        self.account.submit_for_loan(loan)
        assert self.account.balance == expected

    #---------------------------------------------------------------------------#
    
    @pytest.mark.parametrize("balance,inside,expectedB,expectedH", 
        [
            (300.0,300.0,600.0,[300.0])
        ])
    def test_transfer_incoming(self,balance,inside,expectedB,expectedH):
        self.account.balance = balance
        self.account.incoming_transfer(inside)
        assert self.account.balance == expectedB
        assert self.account.history == expectedH
    
    #---------------------------------------------------------------------------#
    
    def test_send_history_email_personal_success(self, mocker):
        self.account.history = [100, -1, 500]

        send_mock = mocker.patch(
            "src.accountPersonal.SMTPClient.send",
            return_value=True
        )

        result = self.account.send_history_via_email("jan@test.pl")

        assert result is True
        send_mock.assert_called_once()

        subject, text, email = send_mock.call_args[0]
        assert subject.startswith("Account Transfer History")
        assert text == "Personal account history: [100, -1, 500]"
        assert email == "jan@test.pl"
    
    #---------------------------------------------------------------------------#

    def test_send_history_email_personal_failure(self, mocker):
        self.account.history = []

        mocker.patch(
            "src.accountPersonal.SMTPClient.send",
            return_value=False
        )

        result = self.account.send_history_via_email("jan@test.pl")

        assert result is False
    
    #---------------------------------------------------------------------------#

