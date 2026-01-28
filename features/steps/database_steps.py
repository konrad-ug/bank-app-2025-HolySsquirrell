from behave import *
import requests

URL = "http://localhost:5000"

@when('I save all accounts to DB')
def save_accounts(context):
    response = requests.post(URL + "/api/accounts/save")
    assert response.status_code == 200

@when('I load all accounts from DB')
def load_accounts(context):
    response = requests.post(URL + "/api/accounts/load")
    assert response.status_code == 200
