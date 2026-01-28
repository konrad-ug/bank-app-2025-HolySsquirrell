import pytest
from unittest.mock import Mock
from src.repository import MongoAccountsRepository
from src.accountPersonal import AccountPersonal

@pytest.fixture
def account1():
    return AccountPersonal("Anna", "Kowalska", "12345678901")

@pytest.fixture
def account2():
    return AccountPersonal("John", "Doe", "11111111111")

def test_save_all(mocker, account1, account2):
    mock_collection = mocker.Mock()
    repo = MongoAccountsRepository()
    repo._collection = mock_collection

    repo.save_all([account1, account2])

    assert mock_collection.delete_many.called
    assert mock_collection.update_one.call_count == 2

def test_load_all(mocker, account1, account2):
    mock_collection = mocker.Mock()
    mock_collection.find.return_value = [
        account1.__dict__, account2.__dict__
    ]
    repo = MongoAccountsRepository()
    repo._collection = mock_collection

    registry = repo.load_all()
    assert len(registry.accounts) == 2
