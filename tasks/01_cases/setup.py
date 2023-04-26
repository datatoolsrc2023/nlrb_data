#!/usr/bin/env python3

from common import db_config, sql
import sys


def main():
    cnx = sql.db_cnx()

    """Create cases table"""

    with sql.db_cnx() as cnx:

        # Create cases table
        with cnx.cursor() as c:
            statements = sql.get_query_lines_from_file('cases.sql')
            try:
                print(f'Creating {db_config.cases} table...')
                for statement in statements:
                    c.execute(statement)
                cnx.commit()
            except Exception as e:
                error = True
                print(f'Failed to create table '
                      f'{db_config.cases}: {e}')
                print('Rolling back')
                cnx.rollback()
                sys.exit(1)


if __name__ == '__main__':
    main()
