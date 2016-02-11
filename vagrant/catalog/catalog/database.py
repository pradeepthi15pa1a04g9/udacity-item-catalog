from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dbfilename = 'catalog.db'

engine = create_engine('sqlite:///%s' % dbfilename)

DBSession = sessionmaker(bind=engine)
db_session = DBSession() # Imported by view module to make queries

Base = declarative_base() # Imported by the models module as base class for models

def init_db():
    import catalog.models
    Base.metadata.create_all(engine)    