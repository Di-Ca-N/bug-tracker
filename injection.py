import inject

from tickets.adapters.storage.ticket_repository import InMemoryTicketRepository
from tickets.adapters.storage.account_repository import InMemoryAccountRepository
from tickets.application.ports import TicketRepository, AccountRepository


def configure_injection(env="dev"):
    def configuration(binder: inject.Binder):
        if env == "dev":
            binder.bind(TicketRepository, InMemoryTicketRepository())
            binder.bind(AccountRepository, InMemoryAccountRepository())
        elif env == "prod":
            pass
        elif env == "test":
            pass
        else:
            raise ValueError("Invalid env")

    inject.configure(configuration)
