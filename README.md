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

### Set up the DB

1. Set up a local MySQL database (actual setup will depend on your OS).
1. Start mysql and create the `nlrb_data` database:
`mysql> create database nlrb_data;`
1. Set up a user:
    * `mysql> CREATE USER IF NOT EXISTS nlrb IDENTIFIED BY 'whateveryourpasswordis';` (change the password)
    * `mysql> GRANT ALL ON nlrb_data.* TO 'nlrb'@'localhost';`
    * `mysql> FLUSH PRIVILEGES;`
1. Create tables, assuming you start MySQL from the top level of the git repo:
    * `mysql> source sql/cases.sql` (or `mysql -u nlrb -p nlrb_data < sql/cases.sql` from your shell)
    * `mysql> source sql/allegations.sql`
1. Rename `db_config-example.py` to `db_config.py` and add your DB username, host, and password.

### Clean CSV files and insert them into the `cases` table

Running `ingest.py` will clean CSV files and insert the data into the cases table. You can run ingest.py in three ways:

- running `ingest.py` with no arguments will clean and load all lines of all CSV files in the `case_files` directory
- running `ingest.py some_file.csv` will clean and load all lines of `some_file.csv`
- running `ingest.py some_file.csv 50` will clean and load the first 50 lines of `some_file.csv`

**Note:** `ingest.py` appends rows to the `cases` table if there are more than zero rows in the table, so if you want to start from an empty table, you will need to truncate the `cases` table before re-running `ingest.py`.

### Process allegations

Running `./allegations.py` will:

* Read each case's `allegations_raw`, when not null or empty
* Attempt to parse any allegations within the text
* Populate the `allegations` table for each allegation found
* Set the case's `allegations_parse_error` to `YES`/`1` if one or more allegations failed to parse.

## Fixing stuff
If you find yourself in a pickle while developing, you can always run `./reset.sh` to reload your data set.
(Currently just the Tesla data.)

This won't help if you changed the SQL files, though.
You'll have to drop those tables and resource the schema files.
