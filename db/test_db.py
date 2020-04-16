import unittest
from db.models import *
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def setUpModule():
    """Create Session"""
    engine = build_db("postgresql://localhost/test-whid.v0", reset = True)
    Session = sessionmaker(bind=engine)
    global s
    s = Session()
    ## initialize objects?
    ## empty db?

def tearDownModule():
    s.close()
    ## empty db?

class TestThingsCRUD(unittest.TestCase):
    """
    Tests CRUD for SQLAlchemy Base Objects w/ Postgres Table
    Order of Tests Matter (C->U->D)
    """

    def test0_create_read_thing(self):
        """Tests Writing + Reading Thing to/from DB"""
        thing = Things(name="WHID Project",
                        defaultplace="Home Desk",
                        defaultduration=datetime.timedelta(hours=1))
        s.add(thing)
        s.commit()
        things = s.query(Things).all()
        assert thing in things

    def test1_update_read_thing(self):
        """Tests Updating + Reading Thing to/from DB"""
        thing = s.query(Things).first()
        thing.defaultplace = "Bedroom Desk"
        s.commit()
        assert s.query(Things).get(thing.id).defaultplace == "Bedroom Desk"

    def test2_delete_read_thing(self):
        """Tests Deleting From DB"""
        thing = s.query(Things).first()
        s.delete(thing)
        s.commit()
        assert thing not in s.query(Things).all()




if __name__ == "__main__":
    unittest.main()
