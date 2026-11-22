import concurrent.futures

from src.domain.exceptions import BankingException
from src.domain.models import Account


def test_concurrent_withdrawals_thread_safety():
    # Account has $600. Max daily withdrawals = 10, withdrawal cap = $200.
    # 10 threads attempt to withdraw $200 simultaneously.
    # Exactly 3 withdrawals should succeed ($600 / $200 = 3), and 7 should fail with InsufficientFunds.
    acc = Account(
        account_id="ACC-CONCURRENT",
        owner_name="Thread Safety Test",
        initial_balance=600.0,
        max_daily_withdrawals=10,
        withdrawal_cap=200.0,
    )

    success_count = 0
    failure_count = 0

    def attempt_withdrawal():
        nonlocal success_count, failure_count
        try:
            acc.withdraw(200.0)
            return True
        except BankingException:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(attempt_withdrawal) for _ in range(10)]
        results = [f.result() for f in futures]

    success_count = sum(1 for r in results if r is True)
    failure_count = sum(1 for r in results if r is False)

    assert success_count == 3
    assert failure_count == 7
    assert acc.balance == 0.0
    assert acc.daily_withdrawal_count == 3
