#!/usr/bin/env python3

from common import db_config, sql
import sys
import psycopg2


if __name__ == '__main__':
    """Confirm cases_raw table has rows"""

    count = 0

    with sql.db_cnx() as cnx:
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
                    print(f'Expected {db_config.cases_raw} to exist,',
                          'but table does not exist')
            except psycopg2.ProgrammingError as e:
                print(f'Could not test for table existence: {e}')

    if error:
        sys.exit(1)
