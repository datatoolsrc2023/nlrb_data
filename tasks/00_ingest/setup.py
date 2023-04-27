#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Ensure cases_raw table is created."""

    count = 0
    error = False

    statements = sql.get_query_lines_from_file('cases_raw.sql')

    cnx = sql.db_cnx()
    c = cnx.cursor()
    try:
        print(f'attempting to create {db_config.cases_raw} table...')
        for statement in statements:
            c.execute(statement)
    except:
        print(f'Failed to create table {db_config.cases_raw}')
        raise
    else: # no exception
        cnx.commit()
    finally:
        cnx.close()
            
