from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from courier.keygen import KeyGen
from .base import DeclarativeBase
from .route import route_message
from .account import Account
from .account_message import AccountMessage
from .tag import Tag, message_tag
from .enums import RecipientType

class Message(DeclarativeBase):

    # table
    __tablename__ = 'message'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    from_account_id =           Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    subject =                   Column(String)  # todo: encrypt subject if possible
    has_body =                  Column(Boolean, nullable=False, default=True)
    attachment_count =          Column(Integer, nullable=False, default=0)
    byte_count =                Column(Integer, nullable=False, default=0)

    # relationships
    from_account =     relationship(Account) # no backref
    account_messages = None #-> AccountMessage.message
    elements =         None #-> MessageElement.message
    routes =           relationship('Route', secondary=route_message, backref='messages')
    tags =             relationship(Tag, secondary=message_tag, order_by='Tag.text', backref='messages')

    # constructor
    def __init__(self, from_account, subject):
        self.subject = subject
        self.from_account = from_account
        self.account_messages = []
        self.elements = []
        self.routes = []
        self.tags = []

    def tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def untag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def seal_all(self):

        routed_accts = []

        # add "from" account
        acct_msg = AccountMessage(self.from_account, RecipientType.From)
        self.account_messages.append(acct_msg)
        routed_accts.append(self.from_account)

        # add "to" accounts
        for route in self.routes:
            accts = route.dereference()
            for acct in accts:
                if acct not in routed_accts:
                    acct_msg = AccountMessage(acct, RecipientType.To)
                    self.account_messages.append(acct_msg)
                    routed_accts.append(acct)

        # generate a 32-byte AES secret key
        aes_key = KeyGen.generate_aes_key()

        # encrypt each message element
        for element in self.elements:
            element._encrypt(aes_key)

        # encrypt the AES key for each recipient
        for acct_msg in self.account_messages:
            acct_msg._encrypt_aes_key(aes_key)