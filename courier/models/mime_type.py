from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .base import DeclarativeBase

class MimeType(DeclarativeBase):

    # table
    __tablename__ = 'mime_type'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    text =                      Column('text_', String, nullable=False)

    # constructor
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text