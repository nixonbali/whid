## Motivation

Testing is good, but this CLI will allow me to work with and test an interface into the system, play with it, put it to use, and try a lot more random walks.

As a programmer, a cli interface is actually how I see myself using this tool for tracking things I'm doing from my computer (e.g. programming, working on this project)


## Initial Ideas

`whid whid-project desk now`
- creates thing `whid-project` if non-existent.
- creates new event, at `desk`, with `endtime` at the current time. If there is a `defaultduration`, the `starttime` is also set (as the current time minus the default duration)
