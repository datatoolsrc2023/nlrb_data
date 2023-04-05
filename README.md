# README

## Setup

### Set up the DB

1. Set up a local MySQL database (actual setup will depend on your OS).
2. Start mysql and create the `nlrb_data` database:
`mysql> create database nlrb_data;`
3. Create the `nlrb_data.cases` table:
`mysql> source /path/to/nlrb_data/sql/cases.sql`

### Clean CSV files and insert them into the `cases` table

Running ingest.py will clean CSV files and insert the data into the cases table. You can run ingest.py in three ways:

- running `ingest.py` with no arguments will clean and load all lines of all CSV files in the `case_files` directory
- running `ingest.py some_file.csv` will clean and load all lines of `some_file.csv`
- running `ingest.py some_file.csv 50` will clean and load the first 50 lines of `some_file.csv`

**Note:** `ingest.py` appends rows to the `cases` table if there are more than zero rows in the table, so if you want to start from an empty table, you will need to truncate the `cases` table before re-running `ingest.py`.
