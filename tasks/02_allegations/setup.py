#!/usr/bin/env python3

from common import db_config, Connection, project_path

import sys

import pymysql


if __name__ == '__main__':
    """Ensure database is created as needed."""

    error = False
    count = 0

    fn = project_path / 'sql' / 'allegations.sql'
    with open(fn, 'r') as f:
        sql = f.read().strip()

    statements = sql.split(';')
    statements = (s.strip() for s in statements)
    statements = (s for s in statements if len(s) > 0)
    statements = (' '.join(s.split()) for s in statements)

    cnx = Connection(db_config)
    cnx.begin()
    c = cnx.cursor()
    try:
        for statement in statements:
            print(statement)
            c.execute(statement)
        print('Committing changes')
        cnx.commit()
    except Exception as e:
        error = True
        print(f'Failed to create table allegations: {e}')
        print('Rolling back')
        cnx.rollback()


    # Clean up gracefully, then exit with error if needed
    c.close()
    cnx.close()

    if error:
        sys.exit(1)
