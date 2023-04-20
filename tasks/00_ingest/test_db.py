#!/usr/bin/env python3

from common import app_config, sql
import sys
import pymysql


if __name__ == '__main__':
    """Confirm cases_raw table has rows"""

    count = 0

    with sql.db_cnx() as cnx:
        with cnx.cursor() as c:
            query = f"""
                    SELECT table_name from information_schema.tables\
                    WHERE table_schema = '{app_config.schema}'\
                    AND table_name = '{app_config.cases_raw}';
                    """

            try:
                result = c.execute(query)
                if result == 0:
                    print(f'Expected {app_config.cases_raw} to have rows,',
                          'but found 0 rows')
                    sys.exit(1)
            except pymysql.err.ProgrammingError as e:
                print('Could not test for existence of ',
                      f'{app_config.cases_raw} table: {e}')
