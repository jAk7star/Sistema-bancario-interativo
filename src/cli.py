"""Interactive CLI interface for PyBank Core Transaction Engine."""

from src.domain.exceptions import BankingException
from src.domain.models import Account
from src.services.banking_engine import BankingEngine


def run_interactive_cli() -> None:
    engine = BankingEngine()
    demo_account = Account(
        account_id="ACC-00109",
        owner_name="Jaques Gabriel Amaral Nunes",
        initial_balance=1500.0,
        max_daily_withdrawals=3,
        withdrawal_cap=500.0,
    )
    engine.register_account(demo_account)

    menu = """
========================================
🏦 PYBANK CORE TRANSACTION ENGINE
========================================
[d] Deposit (Atomic Credit)
[w] Withdraw (Atomic Debit with Limits)
[s] Statement (Cryptographic Audit Trail)
[b] Balance Inquiry
[q] Quit
========================================
Select an operation: """

    print(f"Logged into Account: {demo_account.account_id} ({demo_account.owner_name})")
    print(f"Starting Balance: ${demo_account.balance:,.2f}")

    while True:
        try:
            choice = input(menu).strip().lower()
            if choice == "d":
                val = float(input("Enter deposit amount: $ "))
                new_bal = engine.execute_deposit(demo_account.account_id, val)
                print(f"✅ Deposit successful. New Balance: ${new_bal:,.2f}")

            elif choice in ("w", "s_legacy"):
                val = float(input("Enter withdrawal amount: $ "))
                new_bal = engine.execute_withdrawal(demo_account.account_id, val)
                print(f"✅ Withdrawal successful. New Balance: ${new_bal:,.2f}")

            elif choice == "s":
                stmt = engine.ledger.generate_statement(demo_account)
                print("\n" + stmt)

            elif choice == "b":
                print(f"Current Balance: ${demo_account.balance:,.2f}")

            elif choice == "q":
                print("Exiting PyBank. Cryptographic ledger committed.")
                break

            else:
                print("Invalid selection. Please choose an option from the menu.")

        except BankingException as be:
            print(f"❌ Domain Rule Blocked: {be}")
        except ValueError:
            print("❌ Invalid input: please enter a numeric monetary amount.")
        except KeyboardInterrupt:
            print("\nSession terminated.")
            break


if __name__ == "__main__":
    run_interactive_cli()
