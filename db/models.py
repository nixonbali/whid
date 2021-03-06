from sqlalchemy import Column, ForeignKey, Integer, String, Text, Interval, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    events = relationship('Events')

    @classmethod
    def getThing(cls, session, name, defaultplace=None, defaultduration=None):
        """
        Creates New Thing if First Occurrence of Thing
        Returns Thing by Name
        """
        ## great spot for walrus operator python3.8
        thing = session.query(cls).filter_by(name=name).first()
        if thing:
            return thing
        newThing = cls(name=name, defaultplace=defaultplace, defaultduration=defaultduration)
        session.add(newThing)
        session.commit()
        return newThing

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
    event = relationship('Events') # list because note event_id in Notes table
    # each note can only have one event -> consider adding event_id col

    @classmethod
    def newNote(cls, session, thing_names=[], thing_ids=[], content=None):
        """
        Commit New Note
        + If tied to event - thing_id provided
        + Else: thing_name(s) provided -> Create New Thing(s) if Necessary

        NoteTime Always Now
        """
        note = cls(notetime=datetime.now(), content=content)
        session.add(note)
        session.commit()
        ## Check for names
        if thing_names:
            thing_ids = [Things.getThing(session, name=thing_name).id \
                        for thing_name in thing_names]
        ### Create NoteThings
        for thing_id in thing_ids:
            NoteThings.newNoteThing(session, note_id=note.id, thing_id=thing_id)
        return note



class Events(Base, WHIDBase):
    """
    Events of Things Being Done
    May have note tied directly to it
    """
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    thing_id = Column(Integer, ForeignKey('things.id'), nullable=False)
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    place = Column(String(255))
    note_id = Column(Integer, ForeignKey('notes.id'))
    thing = relationship('Things')

    @classmethod
    def newEvent(cls, session, thing_name, starttime=None, endtime=None, place=None):
                    # usual=False, now=False):
        """
        Commit New Event
        + Commit New Thing if Necessary
        """
        duration = endtime - starttime if (starttime and endtime) else None
        thing = Things.getThing(session, name=thing_name, defaultplace=place, defaultduration=duration)
        starttime = datetime.now() if starttime == None else starttime
        endtime = datetime.now() if endtime == None else endtime
        event = cls(thing_id=thing.id, starttime=starttime,
                    endtime=endtime, place=place)
        session.add(event)
        session.commit()
        return event

    def newNote(self, session, content):
        """Commit New Note Tied to Event"""
        note = Notes.newNote(session, thing_ids = [self.thing_id], content=content)
        self.note_id = note.id
        session.commit()


class NoteThings(Base, WHIDBase):
    """Many-to-Many Notes - Things Relationships"""
    __tablename__ = 'note_things'
    note_id = Column(Integer, ForeignKey('notes.id'), primary_key = True)
    thing_id = Column(Integer, ForeignKey('things.id'), primary_key = True)

    @classmethod
    def newNoteThing(cls, session, note_id, thing_id):
        note_thing = cls(note_id=note_id, thing_id=thing_id)
        session.add(note_thing)
        session.commit()

def reset_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        from db import engine, Session
        reset_tables(engine)
