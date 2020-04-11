# MVP - CLI, Single User
- `whid meditate -hn` (I meditated here now (default location)
- Prompted: `notes?`
- Saves Time, location, topic, eventID
- Saves Note w/ eventID, (topic?)
- Saves Note as txt file?

### Single User Philosophy
I know we live in the age of sharing, transparency, and lack of privacy. However, I want to incentive against habits, goals, ambitions, as status.


## DB
- Relational
- Table: Things
   - ThingID
   - Thing Name
   - Default Place
- Table: Events
  - EventID
  - ThingID
  - Time
  - Place
  - Duration / End Time ?
- Table: Notes
  - NoteID
  - EventID (can be NULL)
  - Time (if EventID NULL)
  - Place (if EventID NULL)
  - Note
- Table: Note Tx
  - NoteID
  - ThingID
- Queries:
  - All events w/in time Range (+breakdown)
  - All topics w/in time range (+breakdown)
  - All notes on topic (+breakdown)
  - All notes in time range (+breakdown)
