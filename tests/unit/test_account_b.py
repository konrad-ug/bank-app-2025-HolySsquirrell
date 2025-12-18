from src.accountBusiness import AccountBusiness
import pytest

class TestTransfers:
    @pytest.fixture(autouse=True, scope="function")
    def account(self):
        self.account = AccountBusiness("tesla","8421577646")

    #---------------------------------------------------------------------------#

    @pytest.mark.parametrize("Name,Nip,expected", 
        [
            ("tesla","8421577646","8421577646"),
            ("tesla","84215776","Invalid"),
        ])
    def test_nip(self,Name,Nip,expected):
        account = AccountBusiness(Name,Nip)
        assert account.nip == expected
        
    #---------------------------------------------------------------------------#

    @pytest.mark.parametrize("balance,out,expectedB,expectedH", 
        [
            (100.0,200.0,100.0,[]),
            (300.0,200.0,100.0,[-200.0]),
        ])
    def test_transfer(self,balance,out,expectedB,expectedH):
        self.account.balance = balance
        self.account.outgoing_transfer(out)
        assert self.account.balance == expectedB
        assert self.account.history == expectedH

    #---------------------------------------------------------------------------#

    @pytest.mark.parametrize("balance,out,expectedB,expectedH", 
        [
            (300.0,300.0,-5.0,[-300.0,-5.0]),
            (300.0,400.0,300.0,[]),
        ])
    def test_transfer_express(self,balance,out,expectedB,expectedH):
        self.account.balance = balance
        self.account.outgoing_transfer_express(out)
        assert self.account.balance == expectedB
        assert self.account.history == expectedH

    #---------------------------------------------------------------------------#

    @pytest.mark.parametrize("history,balance,loan,expectedB,expectedH", 
        [
            ([],50000.0,400.0,50000.0,[]),
            ([-1775.0],500.0,400.0,500.0,[-1775.0]),
            ([-1775.0],1000.0,400.0,1400.0,[-1775.0,400])
        ])
    def test_loan_tests(self,history,balance,loan,expectedB,expectedH):
        self.account.history = history
        self.account.balance = balance
        self.account.take_loan(loan)
        assert self.account.balance == expectedB
        assert self.account.history == expectedH




    
        