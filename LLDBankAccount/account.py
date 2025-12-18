from abc import ABC, abstractmethod
from threading import Lock
from datetime import datetime
from typing import List, Dict


# =======================
# INTEREST STRATEGY
# =======================

class InterestStrategy(ABC):
    @abstractmethod
    def calculate(self, balance: float) -> float:
        pass


class SavingsInterestStrategy(InterestStrategy):
    def calculate(self, balance: float) -> float:
        return balance * 0.04


class NoInterestStrategy(InterestStrategy):
    def calculate(self, balance: float) -> float:
        return 0.0


# =======================
# TRANSACTION ENTITY
# =======================

class Transaction:
    def __init__(self, tx_type: str, amount: float, account_no: str):
        self.tx_type = tx_type
        self.amount = amount
        self.account_no = account_no
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return f"{self.tx_type} | {self.amount} | {self.timestamp}"


# =======================
# ACCOUNT (TEMPLATE METHOD)
# =======================

class Account(ABC):
    def __init__(self, account_no: str, customer_id: str, interest_strategy: InterestStrategy):
        self.account_no = account_no
        self.customer_id = customer_id
        self.balance = 0.0
        self.interest_strategy = interest_strategy
        self.transactions: List[Transaction] = []
        self._lock = Lock()

    def deposit(self, amount: float):
        self._validate_amount(amount)
        with self._lock:
            self.balance += amount
            self._record("DEPOSIT", amount)

    def withdraw(self, amount: float):
        self._validate_amount(amount)
        with self._lock:
            self._check_balance(amount)
            self.balance -= amount
            self._record("WITHDRAW", amount)

    def get_balance(self) -> float:
        return self.balance

    def calculate_interest(self) -> float:
        return self.interest_strategy.calculate(self.balance)

    def _record(self, tx_type: str, amount: float):
        self.transactions.append(Transaction(tx_type, amount, self.account_no))

    def _validate_amount(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    @abstractmethod
    def _check_balance(self, amount: float):
        pass


# =======================
# CONCRETE ACCOUNTS
# =======================

class SavingsAccount(Account):
    def _check_balance(self, amount: float):
        if self.balance < amount:
            raise Exception("Insufficient balance")


class CurrentAccount(Account):
    def _check_balance(self, amount: float):
        pass  # Overdraft allowed


# =======================
# FACTORY PATTERN
# =======================

class AccountFactory:
    @staticmethod
    def create_account(account_type: str, account_no: str, customer_id: str) -> Account:
        if account_type == "SAVINGS":
            return SavingsAccount(
                account_no,
                customer_id,
                SavingsInterestStrategy()
            )
        elif account_type == "CURRENT":
            return CurrentAccount(
                account_no,
                customer_id,
                NoInterestStrategy()
            )
        else:
            raise ValueError("Unsupported account type")


# =======================
# COMMAND PATTERN
# =======================

class TransactionCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class DepositCommand(TransactionCommand):
    def __init__(self, account: Account, amount: float):
        self.account = account
        self.amount = amount

    def execute(self):
        self.account.deposit(self.amount)


class WithdrawCommand(TransactionCommand):
    def __init__(self, account: Account, amount: float):
        self.account = account
        self.amount = amount

    def execute(self):
        self.account.withdraw(self.amount)


class TransferCommand(TransactionCommand):
    def __init__(self, from_account: Account, to_account: Account, amount: float):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def execute(self):
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)


# =======================
# REPOSITORY PATTERN
# =======================

class AccountRepository:
    def __init__(self):
        self._accounts: Dict[str, Account] = {}

    def save(self, account: Account):
        self._accounts[account.account_no] = account

    def get(self, account_no: str) -> Account:
        return self._accounts.get(account_no)


# =======================
# SINGLETON BANK (FACADE)
# =======================

class Bank:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.repository = AccountRepository()
        return cls._instance

    def open_account(self, account_type: str, account_no: str, customer_id: str) -> Account:
        account = AccountFactory.create_account(account_type, account_no, customer_id)
        self.repository.save(account)
        return account

    def execute_transaction(self, command: TransactionCommand):
        command.execute()

    def get_account(self, account_no: str) -> Account:
        return self.repository.get(account_no)


# =======================
# SAMPLE USAGE
# =======================

if __name__ == "__main__":
    bank = Bank()

    acc1 = bank.open_account("SAVINGS", "ACC1001", "CUST1")
    acc2 = bank.open_account("CURRENT", "ACC2001", "CUST2")

    bank.execute_transaction(DepositCommand(acc1, 1000))
    bank.execute_transaction(WithdrawCommand(acc1, 200))
    bank.execute_transaction(TransferCommand(acc1, acc2, 300))

    print("Savings Balance:", acc1.get_balance())
    print("Current Balance:", acc2.get_balance())
    print("Interest on Savings:", acc1.calculate_interest())
    print("Transactions:", acc1.transactions)
