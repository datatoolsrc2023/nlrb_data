#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Ensure error_log table is created."""

    statements = sql.get_query_lines_from_file(f'{db_config.db_type}/error_log.sql')

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to create {db_config.error_log} table...')
            for statement in statements:
                c.execute(statement)
    except Exception as e:
        raise Exception(f'Failed to create table {db_config.error_log}') from e
    else: # no exception
        print(f'Created {db_config.error_log} table')
    finally:
        c.close()
        cnx.close()
