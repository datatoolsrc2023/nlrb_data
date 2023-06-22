SHELL := /bin/bash

all: setup pre task post

clean:
	# make clean
	# call manually to drop pages table
	# and remove the scrape.log
	python3 ./clean.py
	rm scraper.log

setup:
	# make setup
	which python3
	python3 ./setup.py

pre:
	# make pre
	python3 ./test_db.py
	
task:
	# make task
	python3 ./task.py

post:
	# make post
	python3 ./post.py
