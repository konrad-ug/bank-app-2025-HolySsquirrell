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


class MongoAccountsRepository:
    _memory_storage = []

    def __init__(self, uri="mongodb://localhost:27017", db_name="bank_db", collection_name="accounts"):
        self._collection = None
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            client.server_info()
            db = client[db_name]
            self._collection = db[collection_name]
        except Exception:
            pass


    def save_all(self, accounts):
        if self.use_memory:
            MongoAccountsRepository._memory_storage = [
                {
                    "first_name": acc.first_name,
                    "last_name": acc.last_name,
                    "pesel": acc.pesel,
                    "balance": acc.balance,
                    "history": acc.history
                }
                for acc in accounts
            ]
            return
    
        self._collection.delete_many({})
        for acc in accounts:
            self._collection.insert_one({
                "first_name": acc.first_name,
                "last_name": acc.last_name,
                "pesel": acc.pesel,
                "balance": acc.balance,
                "history": acc.history
            })




    def load_all(self):
        registry = AccountRegistry()
        registry.accounts.clear()
    
        data_source = (
            MongoAccountsRepository._memory_storage
            if self.use_memory
            else self._collection.find({})
        )
    
        for data in data_source:
            acc = AccountPersonal(
                first_name=data["first_name"],
                last_name=data["last_name"],
                pesel=data["pesel"]
            )
            acc.balance = data["balance"]
            acc.history = data["history"]
            registry.add_account(acc)
    
        return registry
