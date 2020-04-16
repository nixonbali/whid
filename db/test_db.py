import unittest
from db.models import *
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def setUpModule():
    """Create Session with Empty DB"""
    engine = build_db("postgresql://localhost/test-whid.v0", reset = True)
    Session = sessionmaker(bind=engine)
    global s
    s = Session()
    ## initialize objects?
    ## empty db?

def tearDownModule():
    """Close Session"""
    s.close()
    ## empty db?

class Helpers:
    @staticmethod
    def create_commit_sample_thing():
        thing = Things(name="WHID Project",
                        defaultplace="Home Desk",
                        defaultduration=timedelta(hours=1))
        s.add(thing)
        s.commit()
        return thing

class TestThingsCRUD(unittest.TestCase):
    """
    Tests CRUD for SQLAlchemy Base Objects w/ Postgres Table
    Order of Tests Matter (C->U->D)
    """

    def test0_create_read_thing(self):
        """Tests Writing + Reading Thing to/from DB"""
        thing = Helpers.create_commit_sample_thing()
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

class TestObjectMethods(unittest.TestCase):
    """User Stories"""

    @classmethod
    def setUpClass(cls):
        """Initialize Thing in DB"""
        thing = Helpers.create_commit_sample_thing()

    def test_getThing(self):
        """Tests Things.getThing method"""
        ## Existing Thing
        pre_get_count = s.query(Things).count()
        thing = Things.getThing(s, name="WHID Project", defaultplace=None, defaultduration=None)
        assert s.query(Things).count() == pre_get_count
        ## New Thing
        newthing = Things.getThing(s, name="Meditation", defaultplace="Bedroom Chair", defaultduration=None)
        assert s.query(Things).count() == pre_get_count + 1
        assert newthing in s.query(Things).all()

    def test_newEvent(self):
        """Tests Events.newEvent method"""
        ## Existing Thing
        event = Events.newEvent(s, thing_name="WHID Project",
                                starttime=datetime.now()-timedelta(hours=1),
                                endtime=datetime.now(), place=None)
        assert event in s.query(Events).all()

        # ADD (USUAL, NOW) FEATURE

        ## New Thing
        endtime = datetime.now()
        event = Events.newEvent(s, thing_name="Strength Training",
                                starttime=endtime-timedelta(hours=1),
                                endtime=endtime, place="Home Gym")
        ### check event
        assert event in s.query(Events).all()
        ### check thing
        thing = s.query(Things).filter_by(name="Strength Training").first()
        assert thing is not None
        assert thing.defaultduration == timedelta(hours=1)
        assert thing.defaultplace == "Home Gym"




if __name__ == "__main__":
    unittest.main()
