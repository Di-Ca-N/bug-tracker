from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from enum import Enum
from typing import List


def generate_id():
    return str(uuid4())


@dataclass
class Account:
    username: str
    email: str
    id: str = field(default_factory=generate_id)


@dataclass
class Comment:
    author: Account
    content: str


class TicketStatus(Enum):
    NEW = 'New'
    ASSIGNED = 'Assigned'
    WONT_FIX = 'Won\'t Fix'
    REJECTED = 'Rejected'
    SOLVED = 'Solved'


class TicketType(Enum):
    BUG = 'Bug'
    FEATURE = 'Feature Request'
    ENHANCEMENT = 'Enhancement Proposal'


@dataclass
class Ticket:
    author: Account
    title: str
    description: str
    type: TicketType
    code: str = field(default_factory=generate_id)
    status: TicketStatus = TicketStatus.NEW
    assigned_to: Account = None
    tags: List[str] = field(default_factory=list)
    creation_date: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    comments: List[Comment] = field(default_factory=list)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        super().__setattr__('updated_at', datetime.now())

    def add_comment(self, author: Account, text: str):
        self.comments.append(Comment(author, text))

    def assign_to(self, user: Account):
        self.assigned_to = user
        self.status = TicketStatus.ASSIGNED

    def close(self, closing_status):
        self.status = closing_status
