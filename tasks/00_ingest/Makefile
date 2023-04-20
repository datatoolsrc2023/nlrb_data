SHELL := /bin/bash

all: setup pre task post teardown

clean:
	# Drop cases_raw table
	python3 ./clean.py

setup:
	# Create cases_raw table
	python3 ./setup.py

teardown:
	# Anything that needs to be unset every time

pre:
	# Test that cases_raw table exists
	python3 ./test_db.py

task:
	# Insert data from case CSVs into cases_raw table
	python3 ./task.py


post:
	# Test that cases_raw table has rows
	python3 ./post.py