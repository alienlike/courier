import os.path
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import DeclarativeBase
from .session import DBSession
from courier.fsio import FileSystemIO
from courier.models.mime_type import MimeType
from Crypto.Cipher import AES
from Crypto.Util import Counter
from binascii import b2a_hex, a2b_hex

class MessageElement(DeclarativeBase):

    # table
    __tablename__ = 'message_element'

    # columns
    id =                        Column(Integer, primary_key=True, nullable=False)
    message_id =                Column(Integer, ForeignKey('message.id', ondelete='CASCADE'), nullable=False)
    mime_type_id =              Column(Integer, ForeignKey('mime_type.id'), nullable=False)
    created_date =              Column(DateTime, nullable=False, default=datetime.now)
    modified_date =             Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    byte_count =                Column(Integer, nullable=False)
    sequence =                  Column('sequence_', Integer, nullable=False)
    rel_path =                  Column(String, nullable=False)

    # relationships
    message =   relationship('Message', backref='elements', order_by='MessageElement.sequence')
    mime_type = relationship(MimeType) # no backref

    # todo: use streams to read/write encrypted content directly from/to disk
    content = None

    # constructor
    def __init__(self, content, mime_type):
        # this id is unique in that we need it before anything is flushed to the database;
        # hence we grab it explicitly using arbitrary sql before going any further
        self.id = DBSession.execute("select nextval('message_element_id_seq')").scalar()
        self.content = content
        self.mime_type = mime_type
        self.byte_count = 0
        self.sequence = 0

    def _get_aes_encryptor(self, aes_key):
        # create a 128-bit counter (AES uses 128-bit blocks)
        ctr = Counter.new(128, initial_value=self.id)
        # create an AES encryptor in CTR mode
        aes = AES.new(aes_key, AES.MODE_CTR, counter=ctr)
        return aes

    def _encrypt(self, aes_key):
        # encrypt message element using the AES key
        aes = self._get_aes_encryptor(aes_key)
        if self.content is not None:
            fs = FileSystemIO()
            abspath, relpath = fs.get_path(self.id)
            self.rel_path = relpath
            f = open(abspath, 'wb')
            ciphertext = b2a_hex(aes.encrypt(self.content))
            f.write(ciphertext)
            f.close()
            # make self.content go away now
            self.content = None

    def _decrypt(self, aes_key):
        # decrypt message element using the AES key
        aes = self._get_aes_encryptor(aes_key)
        fs = FileSystemIO()
        path = fs.get_abspath(self.rel_path)
        if os.path.exists(path):
            f = open(path, 'rb')
            ciphertext = f.read()
            f.close()
            self.content = aes.decrypt(a2b_hex(ciphertext))