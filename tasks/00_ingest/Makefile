SHELL := /bin/bash

all: clean setup pre task post

clean:
	# make clean
	# Drop cases_raw table
	python3 ./clean.py

setup:
	# make setup
	# Create cases_raw table
	python3 ./setup.py

pre:
	# make pre
	# Test that cases_raw table exists
	python3 ./test_db.py

task:
	# make task
	# Insert data from case CSVs into cases_raw table
	python3 ./task.py

post:
	# make post
	# Test that cases_raw table has rows
	python3 ./post.py