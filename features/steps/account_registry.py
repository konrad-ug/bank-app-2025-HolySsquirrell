from behave import *
import requests

URL = "http://localhost:5000"


@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {
        "name": name,
        "surname": last_name,
        "pesel": pesel
    }

    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201


@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()

    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")


@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()

    assert len(accounts) == int(count)


@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")

    assert response.status_code == 200
    data = response.json()
    assert data["pesel"] == pesel


@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404


@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200


@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}")

    json_body = { field: value }

    response = requests.patch(
        URL + f"/api/accounts/{pesel}",
        json=json_body
    )

    assert response.status_code == 200


@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")

    assert response.status_code == 200
    data = response.json()

    assert data[field] == value


@when('I transfer "{amount}" from "{sender}" to "{receiver}"')
def make_transfer(context, amount, sender, receiver):
    response = requests.post(
        URL + "/api/transfers",
        json={
            "from": sender,
            "to": receiver,
            "amount": float(amount)
        }
    )
    assert response.status_code == 200


@step('Account "{pesel}" balance is "{amount}"')
def set_balance(context, pesel, amount):
    response = requests.patch(
        URL + f"/api/accounts/{pesel}",
        json={"balance": float(amount)}
    )
    assert response.status_code == 200


@then('Account "{pesel}" balance equals "{amount}"')
def check_balance(context, pesel, amount):
    response = requests.get(URL + f"/api/accounts/{pesel}")

    assert response.status_code == 200
    data = response.json()

    assert float(data["balance"]) == float(amount)
