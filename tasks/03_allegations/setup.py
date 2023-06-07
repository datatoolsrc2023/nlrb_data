#!/usr/bin/env python3

from common import db_config, sql

from psycopg2.extras import DictCursor 


if __name__ == '__main__':
    """Ensure database is created as needed."""

    statements = sql.get_query_lines_from_file(f'{db_config.db_type}/allegations.sql')

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to create {db_config.allegations} table...')
            for statement in statements:
                print(statement)
                c.execute(statement)
    except Exception as e:
        print(f'Failed to create {db_config.allegations} table')
        raise e
    else:
        print(f'Created {db_config.allegations} table')
    finally:
        cnx.close()
