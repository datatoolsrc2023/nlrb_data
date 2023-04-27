#!/usr/bin/env python3

from common import db_config, sql
import sys
import psycopg2

if __name__ == '__main__':
    """Confirm cases table has rows"""

    count = 0

    cnx = sql.db_cnx()
    c = cnx.cursor()

    # Confirm cases table has rows
    query = f"""
            SELECT count(*)
            FROM {db_config.cases};
            """
    try:
        c.execute(query)
        count = c.fetchone()[0]
        if count == 0:
            raise ValueError(f'Expected {db_config.cases} table'
                             'to be populated,'
                             'but found 0 records')
    except:
        print(f'Could not count cases')
        raise
    else: # no exception
        print('table has rows')
    finally:
        cnx.close()
