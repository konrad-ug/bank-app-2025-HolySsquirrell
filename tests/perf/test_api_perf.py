import time

def test_create_and_delete_account_perf(client):
    for i in range(100):
        pesel = f"900000000{i:02d}"

        start = time.perf_counter()
        response_create = client.post(
            "/api/accounts",
            json={"name": "Jan", "surname": "Kowalski", "pesel": pesel}
        )
        elapsed = time.perf_counter() - start
        assert response_create.status_code == 201
        assert elapsed < 0.5, f"Response took too long: {elapsed}s"

        start = time.perf_counter()
        response_delete = client.delete(f"/api/accounts/{pesel}")
        elapsed = time.perf_counter() - start
        assert response_delete.status_code == 200
        assert elapsed < 0.5, f"Response took too long: {elapsed}s"

def test_100_incoming_transfers_perf(client):
    pesel = "12345678910"

    response_create = client.post(
        "/api/accounts",
        json={"name": "Anna", "surname": "Nowak", "pesel": pesel}
    )
    assert response_create.status_code == 201

    for _ in range(100):
        start = time.perf_counter()
        response = client.post(
            f"/api/accounts/{pesel}/transfer",
            json={"amount": 10, "type": "incoming"}
        )
        elapsed = time.perf_counter() - start
        assert response.status_code == 200
        assert elapsed < 0.5, f"Response took too long: {elapsed}s"

    response_get = client.get(f"/api/accounts/{pesel}")
    assert response_get.status_code == 200
    assert response_get.json["balance"] == 1000
