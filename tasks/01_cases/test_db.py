#!/usr/bin/env python3

from common import db_config, sql
import pymysql
import sys

if __name__ == '__main__':
    """Confirm cases table exists."""

    count = 0

    with sql.db_cnx() as cnx:

        # Test that cases table exists
        with cnx.cursor() as c:
            query = f"""
                    SELECT table_name from information_schema.tables\
                    WHERE table_schema = '{db_config.schema}'\
                    AND table_name = '{db_config.cases_raw}';
                    """
            try:
                result = c.execute(query)
                if result == 0:
                    error = True
                    print(f'Expected {db_config.cases_raw} to exist,'
                          'but table does not exist')
                    sys.exit(1)
            except pymysql.err.ProgrammingError as e:
                print(f'Could not test for table existence: {e}')
