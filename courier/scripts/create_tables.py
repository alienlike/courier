import logging
from sqlalchemy import engine_from_config
from courier.scripts import settings
from courier.models import DeclarativeBase, DBSession, db_views, populate_lookups

LOG = False

def main(DBSession, engine):

    # set up logging
    if LOG:
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # build tables & views
    db_views.drop_views(engine)
    DeclarativeBase.metadata.bind = engine
    DeclarativeBase.metadata.drop_all()
    DeclarativeBase.metadata.create_all(engine)
    db_views.build_views(engine)

    # populate lookups
    populate_lookups(DBSession)

if __name__ == '__main__':

    # configure session
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    DBSession.configure(bind=engine)

    main(DBSession, engine)
