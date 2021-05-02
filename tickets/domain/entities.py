from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from enum import Enum
from typing import List


@dataclass
class Account:
    username: str
    email: str


@dataclass
class Comment:
    author: Account
    content: str


@dataclass
class HistoricRegistry:
    class Operations(Enum):
        CREATION = 'creation'
        UPDATE = 'update'
        COMMENT = 'comment'

    operation: Operations
    field: str
    old_value: str = None
    new_value: str = None
    datetime: datetime = field(default_factory=datetime.now, init=False)


class TicketStatus(Enum):
    NEW = 'New'
    NEED_MORE_INFO = 'Need More Info'
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
    code: int
    status: TicketStatus = TicketStatus.NEW
    assigned_to: Account = None
    tags: List[str] = field(default_factory=list)
    closing_message: str = ""
    creation_date: datetime = field(default_factory=datetime.now)
    comments: List[Comment] = field(default_factory=list)
    changes_history: List[HistoricRegistry] = field(default_factory=list)

    def __post_init__(self):
        self.changes_history.append(HistoricRegistry('creation', None, None, None))

    def __setattr__(self, name, value):
        try:
            old_value = getattr(self, name)
            self.changes_history.append(HistoricRegistry('update', name, old_value, value))
        except AttributeError:
            pass

        super().__setattr__(name, value)

    def add_comment(self, author: Account, text: str):
        self.comments.append(Comment(author, text))

    def assign_to(self, user: Account):
        self.assigned_to = user
        self.status = TicketStatus.ASSIGNED

