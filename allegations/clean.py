#!/usr/bin/env python3

import sys, os
sys.path.append(os.getcwd() + '/..')
import db_config

from connection import Connection

import pymysql


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    error = False
    count = 0

    cnx = Connection(db_config)
    cnx.begin()
    c = cnx.cursor()
    try:
        c.execute("DROP TABLE IF EXISTS allegations;")
    except Exception as e:
        error = True
        print(f"Failed to drop allegations: {e}")

    try:
        changed = c.execute('UPDATE cases SET allegations_parse_error = NULL;')
        print(f'Reset allegations_parse_error = NULL for {changed} records')
    except pymysql.err.ProgrammingError as e:
        error = True
        print(f'Failed to reset allegations_parse_error to NULL: {e}')

    cnx.commit()

    # Clean up gracefully, then exit with error if needed
    c.close()
    cnx.close()

    if error:
        sys.exit(1)
