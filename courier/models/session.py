from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

# DBSession is configured in several places for different purposes:
#   for Pyramid app:    __init__.py
#   for unit tests:     tests/__init__.py
#   for useful scripts: scripts/__init__.py
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
