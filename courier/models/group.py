from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Table, DateTime, String
from sqlalchemy.orm import relationship, backref
from .base import DeclarativeBase
from .route import Route
from .enums import RouteType

group_member = Table('group_member', DeclarativeBase.metadata,
    Column('group_id', Integer, ForeignKey('group.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('account_id', Integer, ForeignKey('account.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('created_date', DateTime, nullable=False, default=datetime.now)
)

class Group(Route):

    # table
    __tablename__ = 'group'

    # mapper arguments
    __mapper_args__ = {'polymorphic_identity': RouteType.Group}

    # columns
    id =                        Column(Integer, ForeignKey('route.id'), primary_key=True, nullable=False)
    owner_account_id =          Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    name =                      Column(String, nullable=False)
    public = False
    acl = None

    # relationships
    member_accounts = None #-> Account.groups
    owner_account = relationship('Account', backref=backref('groups_owned', lazy=True))

    def __init__(self, name, owner_account):
        super(Group, self).__init__()
        self.name = name
        self.owner_account = owner_account

    def dereference(self):
        # todo: check role on this route
        return self.member_accounts

    def add(self):
        pass

    def remove(self):
        pass

    def send(self):
        pass