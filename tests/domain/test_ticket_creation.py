from unittest import TestCase

from tickets.domain.entities import Ticket, Account, TicketStatus, TicketType, Comment


class TicketTest(TestCase):
    def setUp(self):
        self.author = Account("user", "user@user.com")
        self.ticket = Ticket(self.author, "Bug", "Bug description", TicketType.BUG, 1)
        self.developer = Account('developer', "developer@task.com")
    
    def test_creation_appears_on_changes_history(self):
        self.assertEqual(len(self.ticket.changes_history), 1)
        self.assertEqual(self.ticket.changes_history[0].operation, 'creation')

    def test_ticket_field_updates_appear_on_changes_history(self):
        self.ticket.title = "New Bug Title"

        self.assertEqual(len(self.ticket.changes_history), 2)

        register = self.ticket.changes_history[1]
        self.assertEqual(register.operation, 'update')
        self.assertEqual(register.field, 'title')
        self.assertEqual(register.old_value, 'Bug')
        self.assertEqual(register.new_value, 'New Bug Title')

    def test_ticket_assignment_updates_status(self):
        self.ticket.assign_to(self.developer)
        self.assertEqual(self.ticket.assigned_to, self.developer)
        self.assertEqual(self.ticket.status, TicketStatus.ASSIGNED)

    def test_ticket_add_comments(self):
        self.ticket.add_comment(self.author, "New info")
        self.assertEqual(len(self.ticket.comments), 1)
        self.assertEqual(self.ticket.comments[0], Comment(self.author, "New info"))

