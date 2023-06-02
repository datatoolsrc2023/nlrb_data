SHELL := /bin/bash

all: sample_cases sample_pages

sample_cases:
	# make sample_data
	# call manually
	unzip "../../data/sample_data/case_files/*.zip"
	mv *.csv ../../data/case_files && rm -r __MACOSX


# call manually to load case files into db,
sample_pages:
	#
	# or from the sample_data dir, extracting as necessary
	cat ../../data/sample_data/page_files/pages.backup.tar.gz.* | tar xzf -
	mv page_files/ ../../data/
	