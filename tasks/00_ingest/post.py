#!/usr/bin/env python3

from common import app_config, sql
import sys
import pymysql


if __name__ == '__main__':
    """Confirm database meets expectations."""

    error = False
    count = 0

    cnx = sql.db_cnx()
    c = cnx.cursor()
    query = f"""
            SELECT count(*)
            FROM {app_config.schema}.{app_config.cases_raw};
            """

    try:
        c.execute(query)
        count = c.fetchone()[0]
        if count == 0:
            error = True
            print(f'Expected {app_config.cases_raw} table to be populated,',
                  'found 0 records')
    except pymysql.err.ProgrammingError as e:
        print(f'Could not count cases: {e}')

    c.close()
    cnx.close()

    if error:
        sys.exit(1)
