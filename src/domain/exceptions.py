"""Domain exceptions for Core Banking Transaction Engine."""


class BankingException(Exception):
    """Base exception for all banking core domain errors."""


class InsufficientFundsError(BankingException):
    """Raised when an account balance cannot cover a debit transaction."""


class ExceededDailyWithdrawalLimitError(BankingException):
    """Raised when a withdrawal exceeds the allowed daily operation count."""


class ExceededTransactionCapError(BankingException):
    """Raised when a single withdrawal amount exceeds policy limits."""


class InvalidAmountError(BankingException):
    """Raised when an amount is negative, zero, or non-finite."""


class LedgerCorruptionError(BankingException):
    """Raised when ledger cryptographic hash-chain validation fails."""
