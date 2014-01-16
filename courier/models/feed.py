from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Table, DateTime, String
from sqlalchemy.orm import relationship, backref
from .base import DeclarativeBase
from .route import Route
from .enums import RouteType

feed_member = Table('feed_member', DeclarativeBase.metadata,
    Column('feed_id', Integer, ForeignKey('feed.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('account_id', Integer, ForeignKey('account.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('created_date', DateTime, nullable=False, default=datetime.now)
)

class Feed(Route):

    # table
    __tablename__ = 'feed'

    # mapper arguments
    __mapper_args__ = {'polymorphic_identity': RouteType.Feed}

    # columns
    id =                        Column(Integer, ForeignKey('route.id'), primary_key=True, nullable=False)
    owner_account_id =          Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    name =                      Column(String, nullable=False)
    public = False
    acl = None

    # relationships
    member_accounts = None #-> Account.groups
    owner_account = relationship('Account', backref=backref('feeds_owned', lazy=True))

    def __init__(self, name, owner_account):
        super(Feed, self).__init__()
        self.name = name
        self.owner_account = owner_account

    def dereference(self):
        # todo: check role on this route
        return self.member_accounts

    def invite(self):
        pass

    def join(self):
        pass

    def uninvite(self):
        pass

    def ban(self):
        pass

    def leave(self):
        pass

    def send(self):
        pass