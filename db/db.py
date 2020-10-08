from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

def create_session(engine_url):
    engine = create_engine(engine_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    Session = sessionmaker(bind=engine)
    return engine, Session

app_engine_url = "sqlite:///whid.db" #"postgresql://localhost/whid.v0"
engine, Session = create_session(app_engine_url)
