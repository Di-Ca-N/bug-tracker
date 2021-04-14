from typing import Dict
from tickets.application.ports import TicketRepository
from tickets.domain.entities import Ticket


class InMemoryTicketRepository(TicketRepository):
    def __init__(self):
        self.tickets: Dict[str, Ticket] = {}

    def save(self, ticket):
        self.tickets[ticket.code] = ticket
        return ticket
    
    def all(self):
        return list(self.tickets.values())

    def get_by_code(self, code):
        return self.tickets.get(code)
    
    def filter_by_tag(self, tag):
        return [ticket for ticket in self.tickets.values() if tag in ticket.tags]

    def filter_by_type(self, type):
        return [ticket for ticket in self.tickets.values() if ticket.type == type]

    def get_tickets_authored_by(self, user):
        if type(user, str):
            return [ticket for ticket in self.tickets.values() if ticket.author.username == user]
        else:
            return [ticket for ticket in self.tickets.values() if ticket.author == user]
