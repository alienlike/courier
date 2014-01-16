from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from .base import DeclarativeBase

class AccountLink(DeclarativeBase):

    # table
    __tablename__ = 'account_link'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    peer_id =                   Column(Integer, ForeignKey('account_link.id'))
    link_id =                   Column(Integer, ForeignKey('link.id', ondelete='CASCADE'), nullable=False)
    from_account_id =           Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    to_account_id =             Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    hidden =                    Column(Boolean, nullable=False, default=False)

    # relationships

    peer =          relationship('AccountLink', remote_side=[id], post_update=True)
    link =          relationship('Link',
        backref=backref('account_links', lazy=True),
        primaryjoin='Link.id==AccountLink.link_id')
    from_account =  relationship('Account',
        backref=backref('account_links', lazy=True),
        primaryjoin='Account.id==AccountLink.from_account_id')
    to_account =    relationship('Account',
        primaryjoin='Account.id==AccountLink.to_account_id') # no backref

    # constructor
    def __init__(self, link, from_account, to_account):
        self.link = link
        self.from_account = from_account
        self.to_account = to_account
        self.hidden = False