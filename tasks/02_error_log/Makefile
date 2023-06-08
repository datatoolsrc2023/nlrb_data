SHELL := /bin/bash

all: setup pre task

clean:
	# make clean
	# Drop error_log table
	python3 ./clean.py

setup:
	# make setup
	# Create error_log table
	python3 ./setup.py

pre:
	# make pre
	# Test that error_log table exists
	python3 ./test_db.py

task:
	# make task
	# Insert case IDs from cases table into error_log table
	python3 ./task.py

post:
	# make post
	# Test that case IDs are in error_log table
	python3 ./post.py
