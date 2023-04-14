#!/usr/bin/env python3

from common import app_config, sql
import sys


if __name__ == '__main__':
    """Ensure database is created as needed."""

    error = False
    count = 0

    statements = sql.get_query_lines_from_file('cases_raw.sql')

    with sql.db_cnx() as cnx:
        cnx.begin()
        with cnx.cursor() as c:
            try:
                print(f'Creating {app_config.cases_raw} table')
                for statement in statements:
                    print(statement)
                    c.execute(statement)
                cnx.commit()
            except Exception as e:
                error = True
                print(f'Failed to create table {app_config.cases_raw}: {e}')
                print('Rolling back')
                cnx.rollback()

    if error:
        sys.exit(1)
