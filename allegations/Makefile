SHELL := /bin/bash

all: setup pre main post teardown

clean:
	# Remove everything
	echo Clean

#.ONESHELL:
setup:
	# Anything that needs to be set up for this specific task
	echo Setup
	which python3

teardown:
	# Anything that needs to be unset every time
	echo Teardown

pre:
	echo Testing parser
	python3 ./test_parser.py
	echo Testing database state
	python3 ./test_db.py

main:
	echo Main


post:
	echo Post
	python3 ./post.py
