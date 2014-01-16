from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .enums import AccountType
from .account import Account

class Person(Account):

    # table
    __tablename__ = 'person'

    # mapper arguments
    __mapper_args__ = {'polymorphic_identity': AccountType.Person}

    # columns
    id =                        Column(Integer, ForeignKey('account.id'), primary_key=True, nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    first_name =                Column(String, nullable=False)
    last_name =                 Column(String, nullable=False)
    email_address =             Column(String)
    mobile_phone =              Column(String)
    organization =              None

    # constructor
    def __init__(self, username, password, recovery_key, first_name, last_name, email_address, mobile_phone):
        super(Person, self).__init__(username, password, recovery_key)
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.mobile_phone = mobile_phone
        self.display_name = self.get_display_name()

    def get_display_name(self):
        return '%s %s' % (self.first_name, self.last_name)