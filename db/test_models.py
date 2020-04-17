import unittest
from datetime import datetime, timedelta
from db.models import *
from db.db import create_session


def setUpModule():
    """Create Session with Empty DB"""
    global session
    session = create_session("postgresql://localhost/test-whid.v0", reset = True)
    ## initialize objects?
    ## empty db?

def tearDownModule():
    """Close Session"""
    session.close()
    ## empty db?

class Helpers:
    @staticmethod
    def create_commit_sample_thing():
        thing = Things(name="WHID Project",
                        defaultplace="Home Desk",
                        defaultduration=timedelta(hours=1))
        session.add(thing)
        session.commit()
        return thing

class TestThingsCRUD(unittest.TestCase):
    """
    Tests CRUD for SQLAlchemy Base Objects w/ Postgres Table
    Order of Tests Matter (C->U->D)
    """

    def test0_create_read_thing(self):
        """Tests Writing + Reading Thing to/from DB"""
        thing = Helpers.create_commit_sample_thing()
        things = session.query(Things).all()
        assert thing in things

    def test1_update_read_thing(self):
        """Tests Updating + Reading Thing to/from DB"""
        thing = session.query(Things).first()
        thing.defaultplace = "Bedroom Desk"
        session.commit()
        assert session.query(Things).get(thing.id).defaultplace == "Bedroom Desk"

    def test2_delete_read_thing(self):
        """Tests Deleting From DB"""
        thing = session.query(Things).first()
        session.delete(thing)
        session.commit()
        assert thing not in session.query(Things).all()

class TestObjectMethods(unittest.TestCase):
    """User Stories"""

    @classmethod
    def setUpClass(cls):
        """Initialize Thing in DB"""
        thing = Helpers.create_commit_sample_thing()
        ## Thing created: 'WHID Project'

    def test_getThing(self):
        """Tests Things.getThing method"""
        ## Existing Thing
        pre_get_count = session.query(Things).count()
        thing = Things.getThing(session, name="WHID Project", defaultplace=None, defaultduration=None)
        assert session.query(Things).count() == pre_get_count
        ## New Thing
        newthing = Things.getThing(session, name="Meditation", defaultplace="Bedroom Chair", defaultduration=None)
        assert session.query(Things).count() == pre_get_count + 1
        assert newthing in session.query(Things).all()

    def test_newEvent(self):
        """Tests Events.newEvent method"""
        ## Existing Thing
        event = Events.newEvent(session, thing_name="WHID Project",
                                starttime=datetime.now()-timedelta(hours=1),
                                endtime=datetime.now(), place=None)
        assert event in session.query(Events).all()

        # ADD (USUAL, NOW) FEATURE

        ## New Thing
        endtime = datetime.now()
        event = Events.newEvent(session, thing_name="Strength Training",
                                starttime=endtime-timedelta(hours=1),
                                endtime=endtime, place="Home Gym")
        ### check event
        assert event in session.query(Events).all()
        ### check thing
        thing = session.query(Things).filter_by(name="Strength Training").first()
        assert thing is not None
        assert thing.defaultduration == timedelta(hours=1)
        assert thing.defaultplace == "Home Gym"
        assert event in thing.events
        assert event.thing == thing

    def test_newNote_newNoteThing(self):
        """Tests Notes.newNote and (subsequently) NoteThings.newNoteThing methods"""
        ## testing with note as string - could move to reading from file first

        ## Single Thing Name
        note = Notes.newNote(session, thing_names = ['WHID Project'],
                            content = "Designing and Testing Note Model")
        assert note in session.query(Notes).all()
        assert len(note.things) == 1 and note.things[0].name == 'WHID Project'

        ## Single Thing ID
        note = Notes.newNote(session, thing_ids = [session.query(Things).filter_by(name="WHID Project").first().id],
                            content = "Testing Note by Single Thing ID")
        assert note in session.query(Notes).all()
        assert len(note.things) == 1 and note.things[0].name == 'WHID Project'

        ## Multiple Thing Names
        note = Notes.newNote(session, thing_names = [thing.name for thing in session.query(Things).all()],
                            content = "Testing Note by Multiple Thing Names")
        assert note in session.query(Notes).all()
        assert len(note.things) == session.query(Things).count()


        ## Multiple Thing IDs
        note = Notes.newNote(session, thing_ids = [thing.id for thing in session.query(Things).all()],
                            content = "Testing Note by Multiple Thing IDs")
        assert note in session.query(Notes).all()
        assert len(note.things) == session.query(Things).count()

    def test_newNote__fromEvent(self):
        event = Events.newEvent(session, thing_name="WHID Project",
                                starttime=datetime.now()-timedelta(hours=1),
                                endtime=datetime.now(), place=None)
        event.newNote(session, content="Testing Event Notes")
        note = session.query(Notes).get(event.note_id)
        assert note.event[0] == event
        assert len(note.things) == 1 and note.things[0] == event.thing



if __name__ == "__main__":
    unittest.main()
