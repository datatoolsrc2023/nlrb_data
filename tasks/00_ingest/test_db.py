#!/usr/bin/env python3

from common import db_config, sql
import sys
import psycopg2


if __name__ == '__main__':
    """Confirm cases_raw table has rows"""

    count = 0

    with sql.db_cnx() as cnx, cnx.cursor() as c:
        query = f"""
                SELECT * FROM pg_tables
                WHERE schemaname = '{db_config.schema}'
                AND tablename = '{db_config.cases_raw}';
                """

        try:
            c.execute(query)
            if not c.fetchone():
                error = True
                print(f'Expected {db_config.cases_raw} to exist,',
                        'but table does not exist')
                sys.exit(1)
        except psycopg2.ProgrammingError as e:
            print(f'Could not test for table existence: {e}')
