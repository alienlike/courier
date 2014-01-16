from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table
from .base import DeclarativeBase

route_message = Table('route_message', DeclarativeBase.metadata,
    Column('route_id', Integer, ForeignKey('route.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('message_id', Integer, ForeignKey('message.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('created_date', DateTime, nullable=False, default=datetime.now)
)

class Route(DeclarativeBase):

    # table
    __tablename__ = 'route'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    route_type_code =           Column(Integer, nullable=False)

    # relationships
    messages = None #-> Message.routes

    # mapper arguments
    __mapper_args__ = {'polymorphic_on': route_type_code}

    # constructor
    def __init__(self):
        pass