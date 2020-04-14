from sqlalchemy import Column, ForeignKey, Integer, String, Text, Interval, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class WHIDBase():
    def __repr__(self):
        return "\n".join([f"{key}: {value}" for key, value in vars(self).items()][1:])

class Things(Base, WHIDBase):
    """Things That User Does"""
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    defaultplace = Column(String(255))
    defaultduration = Column(Interval)
    notes = relationship('Notes', secondary = 'note_things')

class Notes(Base, WHIDBase):
    """
    Notes User Takes
    Tied to things, but not necessarily events
    """
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    notetime = Column(DateTime)
    ## How will I handle time column when updating notes?
    content = Column(Text)
    things = relationship('Things', secondary = 'note_things')

class Events(Base, WHIDBase):
    """
    Events of Things Being Done
    May have note tied directly to it
    """
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    thing_id = Column(Integer, ForeignKey('things.id'), nullable=False)
    # note: want to be able to create new thing
    # if thing does not exist at time of event creation
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    place = Column(String(255))
    note_id = Column(Integer, ForeignKey('notes.id'))

class NoteThings(Base, WHIDBase):
    """Many-to-Many Notes - Things Relationships"""
    __tablename__ = 'note_things'
    note_id = Column(Integer, ForeignKey('notes.id'), primary_key = True)
    thing_id = Column(Integer, ForeignKey('things.id'), primary_key = True)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    engine = create_engine("postgres://localhost/whid.v0")
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)