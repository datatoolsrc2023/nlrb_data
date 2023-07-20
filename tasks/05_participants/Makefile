SHELL := /bin/bash

all: setup pre task post

clean:
	# Undo everything related to the task. Called manually.
	python3 ./clean.py

setup:
	# Anything that needs to be set up for this specific task
	which python3
	python3 ./setup.py

pre:
	# Tests post-setup and pre-main
	echo Testing database state
	python3 ./test_db.py
	echo Testing parser
	python3 ./test_parser.py
	
task:
	python3 ./task.py

post:
	# Tests post-main and pre-teardown
	python3 ./post.py
