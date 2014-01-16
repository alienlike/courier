from .account import Account
from .account_link import AccountLink
from .account_message import AccountMessage
from .enums import AccountType, RecipientType, LinkState
from .message import Message
from .message_element import MessageElement
from .mime_type import MimeType
from .tag import Tag, message_tag
from .system import System
from .organization import Organization
from .person import Person
from .list import List
from .feed import Feed
from .group import Group
from .link import Link
from .route import Route, route_message
from .base import DeclarativeBase
from .session import DBSession

# to be called after tables are built.
# see the following:
#     scripts/create_tables.py
#     tests/__init__.py.
def populate_lookups(session):
    import transaction
    transaction.begin()
    mt1 = MimeType('text/plain')
    mt2 = MimeType('application/octet-stream')
    items = [mt1,mt2]
    map(session.add, items)
    session.flush()
    transaction.commit()