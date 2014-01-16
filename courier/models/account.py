import bcrypt
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4
from Crypto.PublicKey import RSA
from courier.keygen import KeyGen
from .base import DeclarativeBase
from .link import Link
from .group import Group, group_member
from .list import List, list_member
from .feed import Feed, feed_member

bcrypt_complexity = 12

class Account(DeclarativeBase):

    # table
    __tablename__ = 'account'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    account_type_code =         Column(Integer, nullable=False)
    uid =                       Column(String, unique=True, nullable=False)
    username =                  Column(String, unique=True, nullable=False)
    display_name =              Column(String, nullable=False)
    rsa_key_cipher =            Column(String, nullable=False)
    rsa_key_recovery_cipher =   Column(String, nullable=False)
    rsa_public_key =            Column(String, nullable=False)
    password_hash =             Column(String, nullable=False)
    recovery_key_hash =         Column(String, nullable=False)

    # mapper arguments
    __mapper_args__ = {'polymorphic_on': account_type_code}

    # relationships
    tags =             None #-> Tag.account
    account_links =    None #-> AccountLink.from_account
    account_messages = None #-> AccountMessage.recipient_account
    groups_owned = None #-> Group.owner_account
    groups = relationship(Group, secondary=group_member, backref='member_accounts')
    lists_owned = None #-> List.owner_account
    lists = relationship(List, secondary=list_member, backref='member_accounts')
    feeds_owned = None #-> Feed.owner_account
    feeds = relationship(Feed, secondary=feed_member, backref='member_accounts')

    _private_key = None
    _public_key = None

    # constructor
    def __init__(self, username, password, recovery_key):

        # basic attributes
        self.username = username.lower()

        # generate uid
        self.uid = str(uuid4())

        # set password attributes
        self.password_hash = self._hashpw(password, bcrypt.gensalt(bcrypt_complexity))

        # set recovery key attributes
        self.recovery_key_hash = self._hashpw(recovery_key, bcrypt.gensalt(bcrypt_complexity))

        # generate an rsa key pair
        rsa_key = KeyGen.generate_rsa_key()

        # set key attributes
        self.rsa_key_cipher = rsa_key.exportKey('PEM', password)
        self.rsa_key_recovery_cipher = rsa_key.exportKey('PEM', recovery_key)
        self.rsa_public_key = rsa_key.publickey().exportKey('PEM', '')

    #noinspection PyUnresolvedReferences
    def _hashpw(self, password, salt_or_hash):
        return bcrypt.hashpw(password, salt_or_hash)

    def create_link(self, to_account):
        link = Link(self, to_account)
        return link

    def unlock(self, password):
        # decrypt the private key
        self._private_key = RSA.importKey(self.rsa_key_cipher, password)

    def get_private_key(self):
        return self._private_key

    def get_public_key(self):
        if self._public_key is None:
            self._public_key = RSA.importKey(self.rsa_public_key)
        return self._public_key

    def reset_password(self, old_password, new_password):

        if self.validate_password(old_password):

            # change the passcode on the key
            rsa_key = RSA.importKey(self.rsa_key_cipher, old_password)
            self.rsa_key_cipher = rsa_key.exportKey('PEM', new_password)

            # hash the new password
            self.password_hash = self._hashpw(new_password, bcrypt.gensalt(bcrypt_complexity))

    def validate_password(self, password):

        # validate the password
        valid = self._hashpw(password, self.password_hash) == self.password_hash

        # increase the bcrypt complexity on the hashed password if it has increased
        if valid:
            hash_complexity = self.parse_bcrypt_complexity(self.password_hash)
            if hash_complexity < bcrypt_complexity:
                # todo: make sure the updated hash gets persisted
                self.password_hash = self._hashpw(password, bcrypt.gensalt(bcrypt_complexity))

        return valid

    def validate_recovery_key(self, recovery_key):

        # validate the password
        valid = self._hashpw(recovery_key, self.recovery_key_hash) == self.recovery_key_hash

        # increase the bcrypt complexity on the hashed key if it has increased
        if valid:
            hash_complexity = self.parse_bcrypt_complexity(self.recovery_key_hash)
            if hash_complexity < bcrypt_complexity:
                # todo: make sure the updated hash gets persisted
                self.recovery_key_hash = self._hashpw(recovery_key, bcrypt.gensalt(bcrypt_complexity))

        return valid

    def parse_bcrypt_complexity(self, bcrypt_hash):
        # see http://stackoverflow.com/a/6833165/204900
        hash_complexity = int(bcrypt_hash.split('$')[2])
        return hash_complexity