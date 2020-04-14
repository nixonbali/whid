import unittest
from db.declarative import *
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres://localhost/whid.v0")
Session = sessionmaker(bind=engine)
s = Session()
#
class TestObjectsCRUD(unittest.TestCase):
    """Tests CRUD for SQLAlchemy Base Objects w/ Postgres Table """

    def test_create_read_thing(self):
        """Tests Writing + Reading Thing to/from DB"""
        thing = Things(name="WHID Project",
                        defaultplace="Home Desk",
                        defaultduration=datetime.timedelta(hours=1))
        s.add(thing)
        s.commit()
        things = s.query(Things).all()
        assert thing in things

    def test_update_read_thing(self):
        """Tests Updating + Reading Thing to/from DB"""
        thing = s.query(Things).first()
        thing.defaultplace = "Bedroom Desk"
        s.commit()
        assert s.query(Things).get(thing.id).defaultplace == "Bedroom Desk"

    def test_delete_read_thing(self):
        """Tests Deleting From DB"""
        thing = s.query(Things).first()
        s.delete(thing)
        s.commit()
        assert thing not in s.query(Things).all()

if __name__ == "__main__":
    unittest.main()
