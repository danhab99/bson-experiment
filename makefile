.PHONY: run

run:
	node t.js
	DEBUG=1 python parse.py
