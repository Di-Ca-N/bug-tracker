from abc import ABC, abstractmethod
from typing import List, Union
from tickets.domain.entities import Ticket, Account


class TicketRepository(ABC):
    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: str) -> Ticket:
        raise NotImplementedError

    @abstractmethod
    def filter_by_tag(self, tag: str) -> List[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> List[Ticket]:
        raise NotImplementedError
    
    @abstractmethod
    def get_tickets_authored_by(self, user: Union[str, Account]):
        raise NotImplementedError


class AccountRepository(ABC):
    @abstractmethod
    def save(self, account: Account) -> Account:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, account_id: str) -> Account:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_username(self, username: str) -> Account:
        raise NotImplementedError

    @abstractmethod
    def exists_username(self, username: str) -> bool:
        raise NotImplementedError
