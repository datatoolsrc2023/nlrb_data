#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Ensure cases_raw table is created."""

    statements = sql.get_query_lines_from_file(f'{db_config.db_type}/cases_raw.sql')

    try:
        with sql.db_cnx() as cnx:
            # can't use context manager with cursor
            # because sqlite3 cursor object doesn't support it
            c = cnx.cursor()
            print(f'Attempting to create {db_config.cases_raw} table...')
            for statement in statements:
                c.execute(statement)
    except Exception as e:
        print(f'Failed to create table {db_config.cases_raw}')
        raise e
    else: # no exception
        print(f'Created {db_config.cases_raw} table')
    finally:
        c.close()
        cnx.close()
