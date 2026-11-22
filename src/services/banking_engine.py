"""High-level transactional orchestrator for Core Banking Operations."""

import logging
from collections.abc import Callable
from typing import Any

from src.domain.models import Account, EntryType
from src.services.ledger_service import LedgerService

logger = logging.getLogger(__name__)


class BankingEngine:
    """Core transaction engine coordinating accounts, ledgers, and audit events."""

    def __init__(self, ledger_service: LedgerService | None = None) -> None:
        self.ledger = ledger_service or LedgerService()
        self._accounts: dict[str, Account] = {}
        self._listeners: list[Callable[[str, dict[str, Any]], None]] = []

    def register_account(self, account: Account) -> None:
        self._accounts[account.account_id] = account
        logger.info("Registered account %s for owner %s", account.account_id, account.owner_name)

    def get_account(self, account_id: str) -> Account:
        if account_id not in self._accounts:
            raise KeyError(f"Account {account_id} not found in banking system.")
        return self._accounts[account_id]

    def subscribe_event(self, listener: Callable[[str, dict[str, Any]], None]) -> None:
        """Subscribes an event listener for audit/monitoring hooks."""
        self._listeners.append(listener)

    def _emit_event(self, event_name: str, payload: dict[str, Any]) -> None:
        for listener in self._listeners:
            try:
                listener(event_name, payload)
            except Exception as e:
                logger.error("Event listener error on %s: %s", event_name, e)

    def execute_deposit(self, account_id: str, amount: float) -> float:
        """Executes atomic deposit and records ledger entry."""
        account = self.get_account(account_id)
        new_balance = account.deposit(amount)
        entry = self.ledger.record_entry(account, EntryType.CREDIT, amount, new_balance)

        self._emit_event(
            "TRANSACTION_COMPLETED",
            {
                "type": "DEPOSIT",
                "account_id": account_id,
                "amount": amount,
                "new_balance": new_balance,
                "entry_hash": entry.entry_hash,
            },
        )
        return new_balance

    def execute_withdrawal(self, account_id: str, amount: float) -> float:
        """Executes atomic withdrawal and records ledger entry."""
        account = self.get_account(account_id)
        new_balance = account.withdraw(amount)
        entry = self.ledger.record_entry(account, EntryType.DEBIT, amount, new_balance)

        self._emit_event(
            "TRANSACTION_COMPLETED",
            {
                "type": "WITHDRAWAL",
                "account_id": account_id,
                "amount": amount,
                "new_balance": new_balance,
                "entry_hash": entry.entry_hash,
            },
        )
        return new_balance

    def execute_transfer(
        self, from_account_id: str, to_account_id: str, amount: float
    ) -> tuple[float, float]:
        """Executes atomic bilateral transfer with lock acquisition order preventing deadlocks."""
        source = self.get_account(from_account_id)
        target = self.get_account(to_account_id)

        # Consistent lock acquisition order by account_id to prevent deadlocks
        first, second = sorted([source, target], key=lambda a: a.account_id)

        with first._lock:
            with second._lock:
                src_balance = source.withdraw(amount)
                tgt_balance = target.deposit(amount)

                e1 = self.ledger.record_entry(source, EntryType.DEBIT, amount, src_balance)
                e2 = self.ledger.record_entry(target, EntryType.CREDIT, amount, tgt_balance)

        self._emit_event(
            "TRANSFER_COMPLETED",
            {
                "from_account": from_account_id,
                "to_account": to_account_id,
                "amount": amount,
                "source_hash": e1.entry_hash,
                "target_hash": e2.entry_hash,
            },
        )
        return src_balance, tgt_balance
