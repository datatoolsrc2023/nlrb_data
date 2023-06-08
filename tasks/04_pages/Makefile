SHELL := /bin/bash

all: setup pre task post

clean:
	# make clean, call manually
	# Remove empty .html files from scraped pages data
	find ../../data/page_files -size 0 -delete
	python3 ./clean.py

setup:
	# make setup
	which python3
	python3 ./setup.py

load:
	# make load
	python3 ./load.py

pre:
	# make pre
	python3 ./test_db.py

task:
	# make task
	python3 ./task.py


post:
	# make post
	python3 ./post.py
