#!/usr/bin/env python3

from common import Connection, db_config

import sys

import pymysql


if __name__ == '__main__':
    """Confirm database meets expectations."""

    error = False
    count = 0

    cnx = Connection(db_config)
    c = cnx.cursor()
    try:
        c.execute("SELECT COUNT(*) c FROM cases;")
        count = c.fetchone()[0]
        if count == 0:
            error = True
            print('Expected cases table to be populated, found 0 records')
    except pymysql.err.ProgrammingError as e:
        print(f'Could not count cases: {e}')

    try:
        c.execute("SELECT COUNT(*) c FROM participants;")
        count = c.fetchone()[0]
        if count != 0:
            error = True
            print(f"Expected 0 participants, found {count}")
    except pymysql.err.ProgrammingError as e:
        print(f'Could not count cases: {e}')


    c.close()
    cnx.close()

    if error:
        sys.exit(1)
