#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Drop error_log table"""

    query = 'DROP TABLE IF EXISTS error_log'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to drop {db_config.error_log} table...')
            c.execute(query)
    except Exception as e:
        raise Exception(f'Failed to drop {db_config.error_log} table') from e
    else: # no exception
        print(f'Dropped {db_config.error_log} table')
    finally:
        c.close()
        cnx.close()
