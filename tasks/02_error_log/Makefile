SHELL := /bin/bash

all: setup pre task post

clean:
	# make clean
	# Drop error_log table
	python3 ./clean.py

setup:
	# make setup
	# Create error_log table
	python3 ./setup.py

test:
	# make test
	# Test that error_log table exists
	python3 ./test_db.py
