from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def build_db(engine_url, reset=False):
    engine = create_engine(engine_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    if reset:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

app_engine_url = "postgresql://localhost/whid.v0"
reset = (__name__ == "__main__")
session = build_db(app_engine_url, reset)
