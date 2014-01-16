from sqlalchemy import Column, Integer, ForeignKey
from .account import Account
from .enums import AccountType

class System(Account):

    # table
    __tablename__ = 'system'

    # mapper arguments
    __mapper_args__ = {'polymorphic_identity': AccountType.System}

    # columns
    id =            Column(Integer, ForeignKey('account.id'), primary_key=True, nullable=False)
    account =       None
    system_name =   None
    owner =         None
    organization =  None

    # constructor
    def __init__(self, username, password, recovery_key, system_name):
        super(System, self).__init__(username, password, recovery_key)
        self.system_name = system_name
        self.display_name = self.get_display_name()

    def get_display_name(self):
        return self.system_name