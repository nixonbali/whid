import sys
from db.models import Things, Events, Notes

"""
v0 run w/: $ python3 -m cli.main [args]
"""

"""
args:

event [thing_name] [starttime] [endtime=None] [place=None] [duration=None]
-> triggers newEvent
-> asks for Note
-> if yes
- -> opens note.txt in shell text editor
- -> upon save/exit -> triggers Event.newNote(session, content=read(note.txt))

note [thing_names]
-> opens note.txt in shell text editor
-> upon save/exit -> triggers Note.newNote(session, thing_names=[thing_names], content=read(note.txt)
"""

"""
Development Mode: Use Test DB
"""
development = True
if development:
    from db.db import create_session
    engine, Session = create_session("postgresql://localhost/test-whid.v0")
else:
    from db.db import Session
session = Session()


def invalid_input(*args):
    """Handles Invalid Input Argument"""
    print(f"Invalid Action: {sys.argv[1]}")
    print("Action must be in [event, note]")

def new_event(*args):
    """New Event Input"""
    print('creating new event')

def new_note(*args):
    """New Note Input"""
    print('creating new note')

def list_things(*args):
    """Lists Things"""
    print("Things You're Doing:\n")
    print("\n".join(thing.name for thing in session.query(Things).all()))


from collections import defaultdict
switcher = defaultdict(lambda: invalid_input)
switcher['event'] = new_event
switcher['note'] = new_note
switcher['things'] = list_things

if __name__ == "__main__":
    print('whid called\n')
    try:
        switcher[sys.argv[1]](*sys.argv[2:])
    except IndexError:
        print('No Actions Taken')
