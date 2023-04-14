SHELL := /bin/bash

all: setup pre task post teardown

clean:
	# Undo everything related to the task. Called manually.
	echo dropping nlrb_data.cases and nlrb_data.cases_raw_deduped table
	python3 ./clean.py

setup:
	# Anything that needs to be set up for this specific task
	echo creating nlrb_data.cases_raw_deduped and nlrb_data.cases tables
	python3 ./setup.py

teardown:
	# Anything that needs to be unset every time
	echo Dropping nlrb_data.cases_raw_deduped table
	python3 ./teardown.py

pre:
	# Tests post-setup and pre-main
	echo Testing that nlrb_data.cases_raw exists
	python3 ./test_db.py

task:
	python3 ./task.py


post:
	# Tests post-main and pre-teardown
	python3 ./post.py