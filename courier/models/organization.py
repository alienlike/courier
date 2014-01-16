from sqlalchemy import Column, Integer, ForeignKey
from .account import Account
from .enums import AccountType

class Organization(Account):

    # table
    __tablename__ = 'organization'

    # mapper arguments
    __mapper_args__ = {'polymorphic_identity': AccountType.Organization}

    # columns
    id =                 Column(Integer, ForeignKey('account.id'), primary_key=True, nullable=False)
    account =            None
    organization_name =  None
    owner =              None
    members =            None

    # constructor
    def __init__(self, username, password, recovery_key, organization_name):
        super(Organization, self).__init__(username, password, recovery_key)
        self.organization_name = organization_name
        self.display_name = self.get_display_name()

    def get_display_name(self):
        return self.organization_name