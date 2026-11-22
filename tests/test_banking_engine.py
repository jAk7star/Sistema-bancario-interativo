from src.domain.models import Account
from src.services.banking_engine import BankingEngine


def test_transfer_bilateral_atomicity():
    engine = BankingEngine()
    acc_a = Account("ACC-A", "Sender", initial_balance=1000.0)
    acc_b = Account("ACC-B", "Receiver", initial_balance=200.0)
    engine.register_account(acc_a)
    engine.register_account(acc_b)

    events_captured = []
    engine.subscribe_event(lambda name, payload: events_captured.append((name, payload)))

    src_bal, tgt_bal = engine.execute_transfer("ACC-A", "ACC-B", 300.0)
    assert src_bal == 700.0
    assert tgt_bal == 500.0
    assert acc_a.balance == 700.0
    assert acc_b.balance == 500.0

    assert len(events_captured) == 1
    assert events_captured[0][0] == "TRANSFER_COMPLETED"
    assert events_captured[0][1]["amount"] == 300.0
