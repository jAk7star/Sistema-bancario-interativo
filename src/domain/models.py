"""Core Domain entities and cryptographic ledger entries."""

import hashlib
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.domain.exceptions import (
    ExceededDailyWithdrawalLimitError,
    ExceededTransactionCapError,
    InsufficientFundsError,
    InvalidAmountError,
)


class EntryType(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"


@dataclass(frozen=True)
class LedgerEntry:
    entry_id: str
    account_id: str
    entry_type: EntryType
    amount: float
    balance_after: float
    timestamp: datetime
    prev_hash: str
    entry_hash: str = field(init=False)

    def __post_init__(self) -> None:
        raw_payload = (
            f"{self.prev_hash}:{self.entry_id}:{self.account_id}:"
            f"{self.entry_type.value}:{self.amount:.2f}:{self.balance_after:.2f}:"
            f"{self.timestamp.isoformat()}"
        )
        calculated_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()
        object.__setattr__(self, "entry_hash", calculated_hash)


class Account:
    """Thread-safe core banking account with atomic mutation and invariant checks."""

    def __init__(
        self,
        account_id: str,
        owner_name: str,
        initial_balance: float = 0.0,
        max_daily_withdrawals: int = 3,
        withdrawal_cap: float = 500.0,
    ) -> None:
        if initial_balance < 0.0:
            raise InvalidAmountError("Initial balance cannot be negative.")
        self.account_id = account_id
        self.owner_name = owner_name
        self._balance = initial_balance
        self.max_daily_withdrawals = max_daily_withdrawals
        self.withdrawal_cap = withdrawal_cap
        self._daily_withdrawal_count = 0
        self._lock = threading.RLock()

    @property
    def balance(self) -> float:
        with self._lock:
            return self._balance

    @property
    def daily_withdrawal_count(self) -> int:
        with self._lock:
            return self._daily_withdrawal_count

    def deposit(self, amount: float) -> float:
        """Applies a credit mutation atomically."""
        if amount <= 0.0:
            raise InvalidAmountError(f"Deposit amount must be positive. Received: {amount}")

        with self._lock:
            self._balance += amount
            return self._balance

    def withdraw(self, amount: float) -> float:
        """Enforces limits, checks balance, and executes atomic debit mutation."""
        if amount <= 0.0:
            raise InvalidAmountError(f"Withdrawal amount must be positive. Received: {amount}")

        with self._lock:
            if self._daily_withdrawal_count >= self.max_daily_withdrawals:
                raise ExceededDailyWithdrawalLimitError(
                    f"Daily withdrawal limit of {self.max_daily_withdrawals} operations reached."
                )

            if amount > self.withdrawal_cap:
                raise ExceededTransactionCapError(
                    f"Transaction amount ${amount:.2f} exceeds policy cap of ${self.withdrawal_cap:.2f}."
                )

            if amount > self._balance:
                raise InsufficientFundsError(
                    f"Insufficient funds: attempted withdrawal of ${amount:.2f} with balance of ${self._balance:.2f}."
                )

            self._balance -= amount
            self._daily_withdrawal_count += 1
            return self._balance

    def reset_daily_limits(self) -> None:
        """Resets daily counter at start of next business cycle."""
        with self._lock:
            self._daily_withdrawal_count = 0
