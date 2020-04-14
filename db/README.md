## DB

**Notes:** Note tx table needed so notes can be tied to multiple things. Notes need not be tied to an event. Events have note id column for notes that are tied to it.

- Relational


- Table: Things
   - ThingID
   - Thing Name
   - Default Place
   - Default Duration
- Table: Events
  - EventID
  - ThingID
  - Start Time
  - End Time
  - Place
  - Note ID
- Table: Notes
  - NoteID
  - Timestamp
  - Note Content
- Table: Note Things (TX)
  - id
  - NoteID
  - ThingID
- Queries:
  - All events w/in time Range (+breakdown)
  - All topics w/in time range (+breakdown)
  - All notes on topic (+breakdown)
  - All notes in time range (+breakdown)

**Thoughts:**
- Not considering scaling for multiple users right now (see: [single user philosophy](../README.md#single-user-philosophy)).
- Thinking about keeping note content in some alternative store, but for now will leave in relational db with everything else.
