from src.accountBusiness import AccountBusiness
import pytest


class TestAccountBusiness:
    @pytest.fixture(autouse=True)
    def setup_account(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {"subject": {"nip": "8421577646", "statusVat": "Czynny"}}
        }
        mock_response.text = '{"result":{"subject":{"nip":"8421577646","statusVat":"Czynny"}}}'
        mocker.patch("src.accountBusiness.requests.get", return_value=mock_response)

        self.account = AccountBusiness("tesla", "8421577646")

    #---------------------------------------------------------------------------#
    
    @pytest.mark.parametrize("Name,Nip,expected", 
        [
            ("tesla","8421577646","8421577646"),
            ("tesla","84215776","Invalid"),
        ])
    def test_nip(self, mocker, Name, Nip, expected):
        if len(Nip) == 10:
            mock_response = mocker.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "result": {"subject": {"nip": Nip, "statusVat": "Czynny"}}
            }
            mock_response.text = '{"result":{"subject":{"nip":"'+ Nip + '","statusVat":"Czynny"}}}'
            mocker.patch("src.accountBusiness.requests.get", return_value=mock_response)

        account = AccountBusiness(Name, Nip)
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
    
    def test_nip_invalid_statusVat(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {"subject": {"nip": "1111111111", "statusVat": "Zwolniony"}}
        }
        mock_response.text = '{"result":{"subject":{"nip":"1111111111","statusVat":"Zwolniony"}}}'
        mocker.patch("src.accountBusiness.requests.get", return_value=mock_response)

        with pytest.raises(ValueError) as excinfo:
            AccountBusiness("firma test", "1111111111")
        assert str(excinfo.value) == "Company not registered"
        
    #---------------------------------------------------------------------------#
    
    def test_nip_short_no_api_call(self, mocker):
        mock_get = mocker.patch("src.accountBusiness.requests.get")
        account = AccountBusiness("firma test", "12345")
        assert account.nip == "Invalid"
        mock_get.assert_not_called()
        
    #---------------------------------------------------------------------------#
    
    def test_nip_request_exception(self, mocker):
        mocker.patch("src.accountBusiness.requests.get", side_effect=Exception("Connection error"))
        with pytest.raises(ValueError) as excinfo:
            AccountBusiness("firma test", "8421577646")
        assert str(excinfo.value) == "Company not registered"
        
    #---------------------------------------------------------------------------#   
    
    def test_send_history_email_business_success(self, mocker):
        self.account.history = [5000, -1000, 500]

        send_mock = mocker.patch(
            "src.accountBusiness.SMTPClient.send",
            return_value=True
        )

        result = self.account.send_history_via_email("firma@test.pl")

        assert result is True
        send_mock.assert_called_once()

        subject, text, email = send_mock.call_args[0]
        assert subject.startswith("Account Transfer History")
        assert text == "Company account history: [5000, -1000, 500]"
        assert email == "firma@test.pl"
        
    #---------------------------------------------------------------------------#
    
    def test_send_history_email_business_failure(self, mocker):
        self.account.history = []

        mocker.patch(
            "src.accountBusiness.SMTPClient.send",
            return_value=False
        )

        result = self.account.send_history_via_email("firma@test.pl")

        assert result is False
    
    #---------------------------------------------------------------------------#
