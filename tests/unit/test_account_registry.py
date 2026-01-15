from src.accountRegistry import AccountRegistry
from src.accountPersonal import AccountPersonal
import pytest

class TestAccountRegistry:
    @pytest.fixture(autouse=True, scope="function")
    def accountRegistry(self):
        self.accountRegistry = AccountRegistry()
    