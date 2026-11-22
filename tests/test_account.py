import pytest

from src.domain.exceptions import InvalidAmountError
from src.domain.models import Account


def test_account_creation_valid():
    acc = Account(account_id="ACC-01", owner_name="John Doe", initial_balance=500.0)
    assert acc.account_id == "ACC-01"
    assert acc.balance == 500.0
    assert acc.daily_withdrawal_count == 0


def test_account_creation_negative_balance_raises():
    with pytest.raises(InvalidAmountError):
        Account(account_id="ACC-02", owner_name="Jane Doe", initial_balance=-10.0)


def test_account_deposit_success():
    acc = Account(account_id="ACC-03", owner_name="John Doe", initial_balance=100.0)
    new_bal = acc.deposit(250.0)
    assert new_bal == 350.0
    assert acc.balance == 350.0


def test_account_deposit_invalid_amount_raises():
    acc = Account(account_id="ACC-04", owner_name="John Doe", initial_balance=100.0)
    with pytest.raises(InvalidAmountError):
        acc.deposit(0.0)
    with pytest.raises(InvalidAmountError):
        acc.deposit(-50.0)
