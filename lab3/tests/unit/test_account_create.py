from src.account import Account


class TestTransfers:
    def test_transfer_out_correct(self):
        acc = Account('John','Skyrim','12345678901')
        acc.balance = 100.0
        acc.outgoing_transfer(200.0)
        