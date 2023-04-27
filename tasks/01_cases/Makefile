SHELL := /bin/bash

all: setup pre task post teardown

clean:
	# Drop cases table
	python3 ./clean.py

setup:
	# Create cases table
	python3 ./setup.py

teardown:
	# Anything that needs to be unset every time

pre:
	# Test that cases table exists
	python3 ./test_db.py

task:
	# Clean cases data and insert into cases table
	python3 ./task.py


post:
	# Confirm cases table has rows
	python3 ./post.py