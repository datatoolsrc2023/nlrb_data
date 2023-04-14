#!/usr/bin/env python3

from common import app_config, sql
import sys
import pymysql


if __name__ == '__main__':
    """Confirm cases table has rows
        and drop cases_raw_deduped."""

    error = False
    count = 0

    cnx = sql.db_cnx()
    c = cnx.cursor()

    # Confirm cases table has rows
    query = f"""
            SELECT count(*)
            FROM {app_config.schema}.{app_config.cases};
            """

    try:
        c.execute(query)
        count = c.fetchone()[0]
        if count == 0:
            error = True
            print(f'Expected {app_config.cases} table to be populated,',
                  'found 0 records')
    except pymysql.err.ProgrammingError as e:
        print(f'Could not count cases: {e}')

    # Drop cases_raw_deduped table
    query = f"""
            DROP TABLE {app_config.schema}.{app_config.cases_raw_deduped}
            """

    try:
        c.execute(query)
    except pymysql.err.ProgrammingError as e:
        print(f'Could not drop table {app_config.cases_raw_deduped}: {e}')

    c.close()
    cnx.close()

    if error:
        sys.exit(1)
