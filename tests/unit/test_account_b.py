from src.accountBusiness import AccountBusiness
import pytest

class TestTransfers:
    @pytest.fixture(autouse=True, scope="function")
    def account(self):
        self.account = AccountBusiness("tesla","8421577646")

    def test_correct_nip(self):
        account = AccountBusiness("tesla","8421577646")
        assert account.nip == "8421577646"

    def test_wrong_nip(self):
        account = AccountBusiness("tesla","84215776")
        assert account.nip == "Invalid"
    
    def test_transfer_out_wrong(self):
        self.account.balance = 100.0
        self.account.outgoing_transfer(200.0)

    def test_transfer_out_correct(self):
        self.account.balance = 300.0
        self.account.outgoing_transfer(200.0)
        assert self.account.balance == 100.0

    
        