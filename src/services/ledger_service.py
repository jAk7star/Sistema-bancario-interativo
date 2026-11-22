"""Append-only cryptographic ledger service with audit trail verification."""

import logging
import uuid
from datetime import datetime, timezone

from src.domain.exceptions import LedgerCorruptionError
from src.domain.models import Account, EntryType, LedgerEntry

logger = logging.getLogger(__name__)

GENESIS_HASH = "0" * 64


class LedgerService:
    """Manages append-only immutable ledger books and verifies hash integrity."""

    def __init__(self) -> None:
        self._entries: dict[str, list[LedgerEntry]] = {}

    def record_entry(
        self,
        account: Account,
        entry_type: EntryType,
        amount: float,
        balance_after: float,
    ) -> LedgerEntry:
        account_id = account.account_id
        if account_id not in self._entries:
            self._entries[account_id] = []

        history = self._entries[account_id]
        prev_hash = history[-1].entry_hash if history else GENESIS_HASH

        entry = LedgerEntry(
            entry_id=f"ENT-{uuid.uuid4().hex[:12].upper()}",
            account_id=account_id,
            entry_type=entry_type,
            amount=amount,
            balance_after=balance_after,
            timestamp=datetime.now(timezone.utc),
            prev_hash=prev_hash,
        )
        history.append(entry)
        logger.debug(
            "Recorded %s on account %s: $%0.2f (hash: %s)",
            entry_type.value,
            account_id,
            amount,
            entry.entry_hash[:12],
        )
        return entry

    def get_entries(self, account_id: str) -> list[LedgerEntry]:
        return list(self._entries.get(account_id, []))

    def verify_ledger_integrity(self, account_id: str) -> bool:
        """Verifies the unbroken cryptographic chain from genesis to head."""
        history = self._entries.get(account_id, [])
        if not history:
            return True

        expected_prev = GENESIS_HASH
        for idx, entry in enumerate(history):
            if entry.prev_hash != expected_prev:
                raise LedgerCorruptionError(
                    f"Hash broken at index {idx}! Expected prev_hash {expected_prev}, found {entry.prev_hash}"
                )
            expected_prev = entry.entry_hash

        return True

    def generate_statement(self, account: Account) -> str:
        """Generates a formatted bank statement with verified cryptographic integrity."""
        self.verify_ledger_integrity(account.account_id)
        history = self.get_entries(account.account_id)

        lines = [
            "=" * 50,
            f"ACCOUNT STATEMENT: {account.account_id}",
            f"OWNER: {account.owner_name}",
            f"CURRENT BALANCE: ${account.balance:,.2f}",
            "=" * 50,
            f"{'TIMESTAMP (UTC)':<22} | {'TYPE':<7} | {'AMOUNT':>10} | {'BALANCE':>10}",
            "-" * 50,
        ]

        if not history:
            lines.append("No recorded transactions.")
        else:
            for e in history:
                lines.append(
                    f"{e.timestamp.strftime('%Y-%m-%d %H:%M:%S'):<22} | "
                    f"{e.entry_type.value:<7} | "
                    f"${e.amount:>9.2f} | "
                    f"${e.balance_after:>9.2f}"
                )

        lines.append("=" * 50)
        lines.append(f"AUDIT HASH: {history[-1].entry_hash if history else GENESIS_HASH}")
        lines.append("=" * 50)
        return "\n".join(lines)
