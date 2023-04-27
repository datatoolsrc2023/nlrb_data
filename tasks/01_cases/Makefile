SHELL := /bin/bash

all: setup pre task post

clean:
	# make clean
	# Drop cases table
	python3 ./clean.py

setup:
	# make setup
	# Create cases table
	python3 ./setup.py

pre:
	# make pre
	# Test that cases table exists
	python3 ./test_db.py

task:
	# make task
	# Clean cases data and insert into cases table
	python3 ./task.py

post:
	# make post
	# Confirm cases table has rows
	python3 ./post.py