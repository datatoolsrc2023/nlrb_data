# README

## Setup

### Install dependencies
For Mac or Linux systems, all you should need is Python3.
Then, you can run the following:

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

You can call your virtual environment something else,
but the `./venv/` directory is already gitignored for this repo.

### Set up the DB (optional)

This project uses SQLite by default, which requires no additional setup, but if you want to use PostgreSQL, you will need to do the following:

1. Set up a local PostgreSQL database (actual setup will depend on your OS).
1. Start PostgreSQL and create the `nlrb_data` database:
    `postgres=# create database nlrb_data;`
1. Set up a user and make it the owner of the `nlrb_data` database:
    * `postgres=# CREATE USER nlrb WITH PASSWORD 'badpassword';` (change the password)
    * `postgres=# ALTER DATABASE nlrb_data OWNER TO nlrb;`
1. Rename `db_config-example.py` to `db_config.py` and add your DB username, host, and password.

### Run data cleaning and table creation tasks

1. Download desired CSV(s) from the [NLRB case search website](https://www.nlrb.gov/search/case) and move them to the `date/case_files` directory.
1. Change to the tasks directory:
    `$ cd nlrb_data/tasks`
1. cd into each task subdirectory in numerical order and run `make` in each:
    * `$ cd 00_ingest; make` (creates the `cases_raw` table)
    * `$ cd 01_cases; make` (cleans data from the `cases_raw` table and inserts into the `cases` table)
    * `$ cd 02_error_log; make` (creates the `error_log` table)
    * `$ cd 03_allegations; make` (parses raw allegations text for each cases in the `cases` table and creates the `allegations` table)