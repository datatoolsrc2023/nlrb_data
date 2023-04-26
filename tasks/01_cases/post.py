#!/usr/bin/env python3

from common import db_config, sql
import sys
import psycopg2

if __name__ == '__main__':
    """Confirm cases table has rows"""

    error = False
    count = 0

    with sql.db_cnx() as cnx:
        with cnx.cursor() as c:

            # Confirm cases table has rows
            query = f"""
                    SELECT count(*)
                    FROM {db_config.schema}.{db_config.cases};
                    """
            try:
                c.execute(query)
                count = c.fetchone()[0]
                if count == 0:
                    print(f'Expected {db_config.cases} table'
                          'to be populated,'
                          'but found 0 records')
            except (psycopg2.ProgrammingError, psycopg2.OperationalError) as e:
                print(f'Could not count cases: {e}')
                error = True

    # exit gracefully if needed
    if error:
        sys.exit(1)
