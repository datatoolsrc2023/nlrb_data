#!/usr/bin.env python3

from common import Connection, db_config

import sys

import pymysql


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    error = False
    count = 0

    cnx = Connection(db_config)
    cnx.begin()
    c = cnx.cursor()

    try:
        c.execute("DROP TABLE IF EXISTS participants")
    except Exception as e:
        error = True
        print(f"Failed to drop participants: {e}")

    try:
        changed = c.execute("UPDATE cases SET participants_parse_error = NULL;")
        print(f'Reset participants_parse_error = NULL for {changed} records')
    except pymysql.err.ProgrammingError as e:
        error = True
        print(f'Failed to reset participants_parse_error to NULL: {e}')
    
    cnx.commit()

    # Clean up gracefully, then exit with error if needed
    c.close()
    cnx.close()

    if error:
        sys.exit(1)
        