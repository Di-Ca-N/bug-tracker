import inject

from tickets.domain.entities import Account, Ticket, TicketStatus, TicketType
from .ports import AccountRepository, TicketRepository


@inject.autoparams('ticket_repository')
def open_ticket(author: Account, title: str, description: str, ticket_type: str, 
                tags: list = None, ticket_repository: TicketRepository = None):
    if tags is None:
        tags = []
    ticket = Ticket(author=author, title=title, description=description, type=TicketType(ticket_type), tags=tags)
    return ticket_repository.save(ticket)


@inject.autoparams('ticket_repository')
def list_all_tickets(ticket_repository: TicketRepository):
    return ticket_repository.all()


@inject.autoparams('ticket_repository')
def get_ticket(ticket_code: str, ticket_repository: TicketRepository):
    return ticket_repository.get_by_code(ticket_code)


@inject.autoparams('ticket_repository')
def assign_ticket(ticket: Ticket, user: Account, ticket_repository: TicketRepository):
    ticket.assign_to(user)
    return ticket_repository.save(ticket)


@inject.autoparams('ticket_repository')
def change_ticket_status(ticket: Ticket, new_status: TicketStatus, ticket_repository: TicketRepository):
    ticket.status = new_status
    return ticket_repository.save(ticket)


@inject.autoparams('account_repository')
def get_account_by_username(username: str, account_repository: AccountRepository):
    return account_repository.get_by_username(username)


@inject.autoparams('account_repository')
def check_username_exists(username: str, account_repository: AccountRepository):
    return account_repository.exists_username(username)
