import pytest

from app.api import app, registry


@pytest.fixture
def client():
    app.config["TESTING"] = True
    registry.accounts.clear()

    with app.test_client() as client:
        yield client


def test_create_account(client):
    response = client.post("/api/accounts", json={
        "name": "james",
        "surname": "hetfield",
        "pesel": "32345678901"
    })

    assert response.status_code == 201
    assert response.get_json()["message"] == "Account created"

def test_create_account_duplicate_pesel(client):
    pesel = "11122334455"

    response = client.post("/api/accounts", json={
        "name": "Lars",
        "surname": "Ulrich",
        "pesel": pesel
    })
    assert response.status_code == 201

    response = client.post("/api/accounts", json={
        "name": "Kirk",
        "surname": "Hammett",
        "pesel": pesel
    })
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Account with this PESEL already exists"



def test_get_account_by_pesel(client):
    pesel = "32345678901"

    client.post("/api/accounts", json={
        "name": "john",
        "surname": "doe",
        "pesel": pesel
    })

    response = client.get(f"/api/accounts/{pesel}")

    assert response.status_code == 200
    data = response.get_json()

    assert data["name"] == "john"
    assert data["surname"] == "doe"
    assert data["pesel"] == pesel


def test_get_account_not_found(client):
    response = client.get("/api/accounts/999999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Account not found"


def test_patch_account(client):
    pesel = "32345678901"

    client.post("/api/accounts", json={
        "name": "alice",
        "surname": "cooper",
        "pesel": pesel
    })

    response = client.patch(f"/api/accounts/{pesel}", json={
        "name": "alice_updated"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Account updated"

    get_response = client.get(f"/api/accounts/{pesel}")
    data = get_response.get_json()

    assert data["name"] == "alice_updated"
    assert data["surname"] == "cooper"


def test_delete_account(client):
    pesel = "32345678901"

    client.post("/api/accounts", json={
        "name": "bob",
        "surname": "marley",
        "pesel": pesel
    })

    response = client.delete(f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Account deleted"

    get_response = client.get(f"/api/accounts/{pesel}")
    assert get_response.status_code == 404

@pytest.fixture
def account_with_balance(client):
    pesel = "55566778899"
    client.post("/api/accounts", json={"name": "Test", "surname": "User", "pesel": pesel})
    client.post(f"/api/accounts/{pesel}/transfer", json={"amount": 1000, "type": "incoming"})
    return pesel

def test_transfer_incoming(client, account_with_balance):
    response = client.post(f"/api/accounts/{account_with_balance}/transfer", json={
        "amount": 500,
        "type": "incoming"
    })
    assert response.status_code == 200
    data = client.get(f"/api/accounts/{account_with_balance}").get_json()
    assert data["balance"] == 1500  

def test_transfer_outgoing_success(client, account_with_balance):
    response = client.post(f"/api/accounts/{account_with_balance}/transfer", json={
        "amount": 300,
        "type": "outgoing"
    })
    assert response.status_code == 200
    data = client.get(f"/api/accounts/{account_with_balance}").get_json()
    assert data["balance"] == 700  

def test_transfer_outgoing_insufficient(client):
    pesel = "66677889900"
    client.post("/api/accounts", json={"name": "Low", "surname": "Balance", "pesel": pesel})
    response = client.post(f"/api/accounts/{pesel}/transfer", json={
        "amount": 100,
        "type": "outgoing"
    })
    assert response.status_code == 422
    assert response.get_json()["error"] == "Insufficient funds"

def test_transfer_express(client, account_with_balance):
    response = client.post(f"/api/accounts/{account_with_balance}/transfer", json={
        "amount": 200,
        "type": "express"
    })
    assert response.status_code == 200
    data = client.get(f"/api/accounts/{account_with_balance}").get_json()
    assert data["balance"] == 1200  

def test_transfer_unknown_type(client, account_with_balance):
    response = client.post(f"/api/accounts/{account_with_balance}/transfer", json={
        "amount": 50,
        "type": "invalid"
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "Unknown transfer type"
