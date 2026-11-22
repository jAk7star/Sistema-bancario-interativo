import pytest

from src.domain.exceptions import LedgerCorruptionError
from src.domain.models import Account, EntryType, LedgerEntry
from src.services.ledger_service import GENESIS_HASH, LedgerService


def test_ledger_append_and_hash_chain():
    acc = Account(account_id="ACC-L1", owner_name="Ledger Test", initial_balance=1000.0)
    service = LedgerService()

    e1 = service.record_entry(acc, EntryType.CREDIT, 500.0, 1500.0)
    assert e1.prev_hash == GENESIS_HASH
    assert len(e1.entry_hash) == 64

    e2 = service.record_entry(acc, EntryType.DEBIT, 200.0, 1300.0)
    assert e2.prev_hash == e1.entry_hash

    assert service.verify_ledger_integrity(acc.account_id) is True


def test_ledger_tampering_detection():
    acc = Account(account_id="ACC-L2", owner_name="Ledger Test", initial_balance=1000.0)
    service = LedgerService()

    service.record_entry(acc, EntryType.CREDIT, 500.0, 1500.0)
    service.record_entry(acc, EntryType.DEBIT, 200.0, 1300.0)

    # Tamper with the history by replacing an entry with corrupted prev_hash
    history = service._entries[acc.account_id]
    tampered_entry = LedgerEntry(
        entry_id=history[1].entry_id,
        account_id=history[1].account_id,
        entry_type=history[1].entry_type,
        amount=history[1].amount,
        balance_after=history[1].balance_after,
        timestamp=history[1].timestamp,
        prev_hash="corrupted_hash" + "0" * 50,
    )
    history[1] = tampered_entry

    with pytest.raises(LedgerCorruptionError):
        service.verify_ledger_integrity(acc.account_id)
