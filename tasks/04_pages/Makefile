SHELL := /bin/bash

all: setup test task post

clean:
	# make clean, call manually to drop pages table
	python3 ./clean.py

setup:
	# make setup
	which python3
	python3 ./setup.py

test:
	# make test
	python3 ./test_db.py
	
task:
	# make task
	python3 ./task.py

post:
	# make post
	python3 ./post.py
