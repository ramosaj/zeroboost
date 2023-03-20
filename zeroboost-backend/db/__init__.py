from sqlalchemy import * 
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
import os


engine = create_engine(f"postgresql+psycopg2://{os.getenv('PG_USERNAME')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}", connect_args={'client_encoding': 'utf8'})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class Base(DeclarativeBase):
    id = Column(Integer,primary_key=True)
    created_at = Column(DateTime,server_default=func.now())
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())

Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from . import models
    Base.metadata.create_all(bind=engine)