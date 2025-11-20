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
        assert self.account.balance == 100.0

    def test_transfer_out_correct(self):
        self.account.balance = 300.0
        self.account.outgoing_transfer(200.0)
        assert self.account.balance == 100.0
        assert self.account.history == [-200.0]

    def test_transfer_out_express_correct_with_negative_balance_end(self):
        self.account.balance = 300.0
        self.account.outgoing_transfer_express(300.0)
        assert self.account.balance == -1.0
        assert self.account.history == [-1.0,-300.0]

    def test_transfer_out_express_wrong(self):
        self.account.balance = 300.0
        self.account.outgoing_transfer_express(400.0)
        assert self.account.balance == 300.0
        assert self.account.history == []

    
        