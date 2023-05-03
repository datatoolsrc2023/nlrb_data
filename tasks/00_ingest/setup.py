#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Ensure cases_raw table is created."""

    statements = sql.get_query_lines_from_file('cases_raw.sql')

    try:
        with sql.db_cnx() as cnx, cnx.cursor() as c:
            print(f'Attempting to create {db_config.cases_raw} table...')
            for statement in statements:
                c.execute(statement)
    except Exception as e:
        raise Exception(f'Failed to create table {db_config.cases_raw}') from e
    else: # no exception
        print(f'Created {db_config.cases_raw} table')
    finally:
        cnx.close()
            
