import pytest

from src.domain.exceptions import (
    ExceededDailyWithdrawalLimitError,
    ExceededTransactionCapError,
    InsufficientFundsError,
)
from src.domain.models import Account


def test_withdrawal_cap_enforced():
    acc = Account(
        account_id="ACC-P1", owner_name="Policy Test", initial_balance=2000.0, withdrawal_cap=500.0
    )
    with pytest.raises(ExceededTransactionCapError):
        acc.withdraw(500.01)


def test_insufficient_funds_enforced():
    acc = Account(account_id="ACC-P2", owner_name="Policy Test", initial_balance=300.0)
    with pytest.raises(InsufficientFundsError):
        acc.withdraw(350.0)


def test_max_daily_withdrawals_limit_enforced():
    acc = Account(
        account_id="ACC-P3",
        owner_name="Policy Test",
        initial_balance=2000.0,
        max_daily_withdrawals=3,
        withdrawal_cap=500.0,
    )
    acc.withdraw(100.0)
    acc.withdraw(100.0)
    acc.withdraw(100.0)
    assert acc.daily_withdrawal_count == 3
    assert acc.balance == 1700.0

    # 4th withdrawal should fail
    with pytest.raises(ExceededDailyWithdrawalLimitError):
        acc.withdraw(50.0)

    # After reset, withdrawal succeeds
    acc.reset_daily_limits()
    assert acc.daily_withdrawal_count == 0
    acc.withdraw(50.0)
    assert acc.balance == 1650.0
