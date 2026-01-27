import pytest
from src.accountRegistry import AccountRegistry
from src.accountPersonal import AccountPersonal


@pytest.fixture
def registry():
    return AccountRegistry()


@pytest.fixture
def accs():
    return [
        AccountPersonal("Jan", "Kowalski", "12345678901"),
        AccountPersonal("Anna", "Nowak", "10987654321"),
        AccountPersonal("Piotr", "Zielinski", "11111111111")
    ]


class TestAccountRegistry:

    @pytest.mark.parametrize(
        "pesel_input,expected_index",
        [
            ("12345678901", 0),
            (12345678901, 0),
            ("10987654321", 1),
            ("00000000000", None)
        ]
    )
    def test_search_account(self, registry, accs, pesel_input, expected_index):
        for acc in accs:
            registry.add_account(acc)

        result = registry.search_account(pesel_input)

        if expected_index is None:
            assert result is None
        else:
            assert result == accs[expected_index]

    def test_add_account(self, registry, accs):
        registry.add_account(accs[0])
        assert registry.return_all_accs() == [accs[0]]

    def test_add_multiple_accounts(self, registry, accs):
        for acc in accs:
            registry.add_account(acc)

        assert registry.return_all_accs() == accs

    @pytest.mark.parametrize("count", [0, 1, 3])
    def test_return_all_accounts_size(self, registry, accs, count):
        for acc in accs[:count]:
            registry.add_account(acc)

        assert len(registry.return_all_accs()) == count

    def test_registry_starts_empty(self, registry):
        assert registry.return_all_accs() == []
