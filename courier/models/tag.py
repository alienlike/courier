from datetime import datetime
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from .base import DeclarativeBase
from courier.models.account import Account

message_tag = Table('message_tag', DeclarativeBase.metadata,
    Column('message_id', Integer, ForeignKey('message.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('created_date', DateTime, nullable=False, default=datetime.now)
)

class Tag(DeclarativeBase):

    # table
    __tablename__ = 'tag'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    account_id =                Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    text =                      Column('text_', String, nullable=False)

    # relationships
    messages =  None #-> Message.tags
    account =   relationship(Account, backref=backref('tags', lazy=True))

    # constructor
    def __init__(self, text, account):
        self.text = text
        self.account = account

    def __repr__(self):
        return self.text