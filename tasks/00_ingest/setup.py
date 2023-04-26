#!/usr/bin/env python3

from common import db_config, sql
import sys


if __name__ == '__main__':
    """Ensure cases_raw table is created."""

    count = 0

    statements = sql.get_query_lines_from_file('cases_raw.sql')

    with sql.db_cnx() as cnx, cnx.cursor() as c:
        try:
            print(f'Creating {db_config.cases_raw} table...')
            for statement in statements:
                c.execute(statement)
        except Exception as e:
            print(f'Failed to create table {db_config.cases_raw}: {e}')
            print('Rolling back')
            sys.exit(1)
