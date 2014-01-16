from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from binascii import b2a_hex, a2b_hex
from .base import DeclarativeBase
from .account import Account
from .enums import RecipientType, FromTo

class AccountMessage(DeclarativeBase):

    # table
    __tablename__ = 'account_message'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    message_id =                Column(Integer, ForeignKey('message.id', ondelete='CASCADE'), nullable=False)
    recipient_account_id =      Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    recipient_type_code =       Column(Integer, nullable=False)
    from_to =                   Column(Integer, nullable=False)
    read =                      Column('read_', Boolean, nullable=False, default=False)
    archived =                  Column(Boolean, nullable=False, default=False)
    aes_key_cipher =            Column(String, nullable=False)

    # mapper arguments
    __mapper_args__ = {'polymorphic_on': from_to}

    # relationships
    message =           relationship('Message', backref='account_messages')
    recipient_account = relationship(Account, backref=backref('account_messages'))

    # constructor
    def __init__(self, recipient_account, recipient_type_code):
        self.recipient_account = recipient_account
        self.recipient_type_code = recipient_type_code
        self.from_to = FromTo.From if recipient_type_code == RecipientType.From else FromTo.To
        self.read = recipient_type_code == RecipientType.From
        self.archived = False

    def _encrypt_aes_key(self, aes_key):

        # get the recipient's public key
        rsa_public_key = self.recipient_account.get_public_key()

        # encrypt the AES key using public key
        self.aes_key_cipher = b2a_hex(rsa_public_key.encrypt(aes_key, '')[0])

    def unseal(self, auth_account):

        # get authenticated user's private key
        rsa_key = auth_account.get_private_key()

        # decrypt AES key using private key
        aes_key = rsa_key.decrypt(a2b_hex(self.aes_key_cipher))

        # decrypt each message element
        for element in self.message.elements:
            element._decrypt(aes_key)