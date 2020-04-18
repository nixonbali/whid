# WHID
An app/service for remembering what you've done, tracking what you're doing, and figuring out what you might do next.

## v0
A Habit (Notes + Events) Tracking CLI

**From whid directory:**
- `python3 -m cli.main event [thing_name]` - creates new event (and new thing if thing_name does not exist yet)
- `python3 -m cli.main things` - lists things you have done

## Philosophy
I want to know what I've been doing. A habit tracker of sorts, that does not get in the way or obligate me to add an extra inconvenience to the set up / tear down involved in my activities. Ease of access, with all the details necessary, and none unnecessary.

### Single User Philosophy
I know we live in the age of sharing, transparency, and lack of privacy. However, I want to incentive against habits, goals, ambitions, as status.

### Things Must have Notes or Events
Rather than adding something you want to do. Things will only be added at the creation of a new event or note for a new thing.

### Basics
-  **Things** that you are doing
- **Noting** if and when things are done
  - **Thing** you've done
  - **When** you did it
  - **Where** you did it
  - **Thoughts** on it

## User Stories
- I meditated
   - Tap / Enter Meditation Event (*perhaps with some details, see noting basics*)
   - Prompted to enter more details (*noting basics*)
- I want to know how often, when, where I meditated
 - Tap / Enter meditation topic
 - Breakdown and notes provided
- I want to know what I've done this week
  - Tap / Enter Time Range
  - Breakdown and notes provided
- I want to enter thoughts on topic
  - Tap / Enter topic & Thoughts
  - Enter thoughts

### Where did I leave off
I want to know at what point in a chapter, project, (sub)task, I left off and what I might be doing next. Not sure whether this ought to be a integrated into each event, have a separate type of event, or have a separate type of **thing** that will allow this (e.g. I may not care where I leave off meditating (*thought I suppose I may*) where as with a book, project, etc. I may want to check what the last thing I did exactly was so I know where to start again, but also can check progress).

## Additional Thoughts
- Group topics by ambition
  - e.g. Web App Project
    - Front-End Work
    - DB Design
    - etc
  - e.g. Mathematics Self Education
    - Linear Algebra Textbook notes
    - Proofs / Exercises
    - Applied Example
    - etc.
- Front End(s)
  - CLI
  - Web App
  - Mobile App
    - Lock Screen Accessible
    - Widget
- Adding multiple topics to random note
- Calendar
  - Integration?
  - Built-in calendar?
