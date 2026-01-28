from abc import ABC, abstractmethod
from pymongo import MongoClient
from src.accountRegistry import AccountRegistry
from src.accountPersonal import AccountPersonal

class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self, accounts):
        pass

    @abstractmethod
    def load_all(self):
        pass


class MongoAccountsRepository(AccountsRepository):
    def __init__(self, uri="mongodb://localhost:27017", db_name="bank_db", collection_name="accounts"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self._collection = self.db[collection_name]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for acc in accounts:
            self._collection.update_one(
                {"pesel": acc.pesel},
                {"$set": acc.__dict__}, 
                upsert=True
            )

    def load_all(self):
        registry = AccountRegistry()
        registry.accounts.clear()

        for data in self._collection.find({}):
            acc = AccountPersonal(
                first_name=data["first_name"],
                last_name=data["last_name"],
                pesel=data["pesel"]
            )
            acc.balance = data["balance"]
            acc.history = data["history"]
            registry.add_account(acc)
        return registry
