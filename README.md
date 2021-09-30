# bson-py

A standard Binary JSON-like parser created to [these specs](https://bsonspec.org/spec.html). I made this in a night because I was bored, it was a highly enlightening experience.

## Demonstration instructions

1. Install node modules with `npm install`
2. Run `node generate.js` to generate a valid bson file
3. Run `python parse.py` to observe outputs

> Run `DEBUG=1 python parse.py` to get a verbose activity log of every read and for what purpose
