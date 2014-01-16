from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .enums import LinkState, RouteType
from .account_link import AccountLink
from .route import Route

class Link(Route):

    # table
    __tablename__ = 'link'

    # mapper arguments
    __mapper_args__ = {'polymorphic_identity': RouteType.Link}

    # columns
    id =                        Column(Integer, ForeignKey('route.id'), primary_key=True, nullable=False)
    origin_account_id =         Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    link_state_code =           Column(Integer, nullable=False)

    # relationships
    account_links =  None #-> AccountLink.link
    origin_account = relationship('Account') # no backref

    # constructor
    def __init__(self, origin_account, to_account):
        super(Link, self).__init__()
        self.origin_account = origin_account
        self.link_state_code = LinkState.Pending
        # create two account links
        al1 = AccountLink(self, origin_account, to_account)
        al2 = AccountLink(self, to_account, origin_account)
        al1.peer = al2
        al2.peer = al1
        self.account_links = [al1, al2]

    def dereference(self):
        # todo: check role on this route
        al = self.account_links[0]
        accts = [al.from_account, al.to_account]
        return accts

    def initiate(self):
        pass

    def withdraw(self):
        pass

    def approve(self):
        pass

    def deny(self):
        pass

    def break_(self):
        pass

    def send(self):
        pass