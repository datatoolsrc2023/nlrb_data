#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Ensure database is created as needed."""

    statements = sql.get_query_lines_from_file('participants.sql')

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to create {db_config.participants} table')
            for statement in statements:
                print(statement)
                c.execute(statement)
    except Exception as e:
        print(f'Failed to create {db_config.participants} table')
        raise e
    else:
        print(f'Created {db_config.participants} table')
    finally:
        c.close()
        cnx.close()
