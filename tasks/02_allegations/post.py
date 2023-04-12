#!/usr/bin/env python3

from common import db_config, Connection

import sys

import pymysql


if __name__ == '__main__':
    """Confirm no records require attention."""

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
        c.execute("SELECT COUNT(*) c FROM allegations WHERE parse_error = 1;")
        count = c.fetchone()[0]
        if count != 0:
            error = True
            print(f"Expected 0 parse errors, found {count}")
            c.execute("""SELECT c.case_number, a.raw_text
                      FROM cases c
                      INNER JOIN allegations a
                      ON c.id = a.case_id
                      WHERE a.parse_error = 1;
                      """)
            for case_number, raw_text in c.fetchall():
                print(f'Case: {case_number} Raw text: {raw_text}')
    except pymysql.err.ProgrammingError as e:
        print(f'Could not summarize parse errors: {e}')


    c.close()
    cnx.close()

    if error:
        sys.exit(1)
