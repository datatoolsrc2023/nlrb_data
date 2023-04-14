#!/usr/bin/env python3

from common import app_config, sql
import sys
import pymysql


if __name__ == '__main__':
    """Confirm database meets expectations."""

    error = False
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
                    error = True
                    print(f'Expected {app_config.cases_raw} to exist,',
                          'but table does not exist')
            except pymysql.err.ProgrammingError as e:
                print(f'Could not test for table existence: {e}')

    if error:
        sys.exit(1)
