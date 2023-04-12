#!/usr/bin/env python3

from common import db_config, Connection, sql

import sys

import pymysql


if __name__ == '__main__':
    """Ensure database is created as needed."""

    error = False
    count = 0

    statements = sql.get_query_lines_from_file('participants.sql')

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
        print(f'Failed to create table participants: {e}')
        print('Rolling back')
        cnx.rollback()