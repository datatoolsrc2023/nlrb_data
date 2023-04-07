#!/usr/bin/env python3

import sys, os
sys.path.append(os.getcwd() + '/..')
import db_config

from connection import Connection

import pymysql


if __name__ == '__main__':
    """Confirm database meets expectations."""

    error = False
    count = 0

    cnx = Connection(db_config)
    c = cnx.cursor()
    try:
        c.execute("SELECT COUNT(*) c FROM cases;")
        count = c.fetchone()['c']
        if count == 0:
            error = True
            print('Expected cases table to be populated, found 0 records')
    except pymysql.err.ProgrammingError as e:
        print(f'Could not count cases: {e}')

    try:
        c.execute("SELECT COUNT(*) c FROM allegations;")
        count = c.fetchone()['c']
        if count != 0:
            error = True
            print(f"Expected 0 allegations, found {count}")
    except pymysql.err.ProgrammingError as e:
        print(f'Could not count cases: {e}')


    c.close()
    cnx.close()

    if error:
        sys.exit(1)
