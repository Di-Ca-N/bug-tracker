from typing import Dict

from tickets.application.ports import AccountRepository
from tickets.domain.entities import Account


class InMemoryAccountRepository(AccountRepository):
    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def save(self, account: Account) -> Account:
        self.accounts[account.id] = account

    def get_by_id(self, account_id: str) -> Account:
        return self.accounts[account_id]

    def get_by_username(self, username: str) -> Account:
        accounts = [account for account in self.accounts.values() if account.username == username]
        if len(accounts) != 1:
            raise Exception("There is more than one account")
        else:
            return accounts[0]

    def exists_username(self, username: str) -> bool:
        return any([account.username == username for account in self.accounts.values()])
