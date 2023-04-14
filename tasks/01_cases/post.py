#!/usr/bin/env python3

from common import app_config, sql
import sys
import pymysql


if __name__ == '__main__':
    """Confirm cases table has rows
        and drop cases_raw_deduped."""

    error = False
    count = 0

    with sql.db_cnx() as cnx:
        with cnx.cursor() as c:

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
                    print(f'Expected {app_config.cases} table'
                          'to be populated,'
                          'but found 0 records')
            except pymysql.err.ProgrammingError as e:
                print(f'Could not count cases: {e}')

    if error:
        sys.exit(1)
