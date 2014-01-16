import os, sqlparse
from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.exc import ProgrammingError
from courier.models.base import DeclarativeBase
from pkg_resources import resource_filename

# COUNTS FOR INBOX TABS AND PAGING

# should account for: hidden, archived, tag subset, contact subset, any, none
total_recd_ct = Table('total_recd_ct', DeclarativeBase.metadata,
    Column('to_account_id', Integer),
    Column('ct', Integer)
)

# should account for: hidden, archived, tag subset, contact subset, any, none
total_sent_ct = Table('total_sent_ct', DeclarativeBase.metadata,
    Column('from_account_id', Integer),
    Column('ct', Integer)
)

# should account for: hidden, archived, tag subset, contact subset, any, none
unread_recd_ct = Table('unread_recd_ct', DeclarativeBase.metadata,
    Column('to_account_id', Integer),
    Column('ct', Integer)
)

# COUNTS FOR CONTACTS PANEL

# should account for: hidden, archived, both, neither
unread_recd_ct_by_link = Table('unread_recd_ct_by_link', DeclarativeBase.metadata,
    Column('to_account_id', Integer),
    Column('from_account_id', Integer),
    Column('from_display_name', String),
    Column('ct', Integer),
    Column('hidden', Boolean)
)

# COUNTS FOR TAGS PANEL

# should account for: hidden, archived, both, neither
unread_recd_ct_by_tag = Table('unread_recd_ct_by_tag', DeclarativeBase.metadata,
    Column('to_account_id', Integer),
    Column('tag_id', Integer),
    Column('tag_text', String),
    Column('ct', Integer)
)

# FLATTENED MESSAGE INFO FOR INBOX - MAY BE JOINED TO TAGS AND/OR ACCTS

v_message_sent = Table('v_messages_sent', DeclarativeBase.metadata,
    Column('message_id', Integer),
    Column('account_message_id', Integer),
    Column('to_account_id', Integer),
    Column('to_display_name', String),
    Column('from_account_id', Integer),
    Column('from_display_name', String),
    Column('account_link_id', Integer),
    Column('hidden', Boolean),
    Column('archived', Boolean)
)

v_message_recd = Table('v_messages_recd', DeclarativeBase.metadata,
    Column('message_id', Integer),
    Column('account_message_id', Integer),
    Column('from_account_id', Integer),
    Column('from_display_name', String),
    Column('to_account_id', Integer),
    Column('to_display_name', String),
    Column('account_link_id', Integer),
    Column('hidden', Boolean),
    Column('archived', Boolean),
    Column('read_', Boolean)
)

# database view management
#
# usage:
#
#    db_views.drop_views(engine)
#    DeclarativeBase.metadata.bind = engine
#    DeclarativeBase.metadata.drop_all()
#    DeclarativeBase.metadata.create_all(engine)
#    db_views.build_views(engine)

_view_names = []
_dir = os.path.dirname(resource_filename(__name__, 'ignoreme')) # the filename given is bogus but the api requires it
for item in os.listdir(_dir):
    if item.endswith('.ddl'):
        name = item.replace('.ddl','')
        _view_names.append(name)

def drop_views(engine):
    for name in _view_names:
        drop_ddl = 'drop view if exists %s' % name
        try:
            engine.execute(drop_ddl)
        except ProgrammingError:
            pass

def _drop_alchemy_tables(engine):
    for name in _view_names:
        drop_ddl = 'drop table if exists %s' % name
        try:
            engine.execute(drop_ddl)
        except ProgrammingError:
            pass

def build_views(engine):

    # drop unwanted tables (where mappings exist, alchemy will have created tables)
    _drop_alchemy_tables(engine)

    for name in _view_names:

        # get view create ddl
        path = os.path.join(_dir, '%s.ddl' % name)
        file = open(path, 'r')
        create_ddl = file.read()
        file.close()

        # strip out comments, then create view according to its ddl
        create_ddl = sqlparse.format(create_ddl, strip_comments=True)
        engine.execute(create_ddl)