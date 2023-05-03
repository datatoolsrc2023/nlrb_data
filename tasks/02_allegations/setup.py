#!/usr/bin/env python3

from common import db_config, sql

from psycopg2.extras import DictCursor 


if __name__ == '__main__':
    """Ensure database is created as needed."""

    statements = sql.get_query_lines_from_file('allegations.sql')

    try:
        with sql.db_cnx(cursor_factory=DictCursor) as cnx, cnx.cursor() as c:
            print(f'Attempting to create {db_config.allegations} table')
            for statement in statements:
                print(statement)
                c.execute(statement)
    except Exception as e:
        raise Exception(f'Failed to create {db_config.allegations} table') from e
    else:
        print(f'Created {db_config.allegations} table')
    finally:
        cnx.close()
