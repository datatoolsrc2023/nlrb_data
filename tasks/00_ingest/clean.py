#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Drop cases_raw table"""

    query = 'DROP TABLE IF EXISTS cases_raw'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to drop {db_config.cases_raw} table...')
            c.execute(query)
    except Exception as e:
        raise Exception(f'Failed to drop {db_config.cases_raw} table') from e
    else: # no exception
        print(f'Dropped {db_config.cases_raw} table')
    finally:
        c.close()
        cnx.close()
