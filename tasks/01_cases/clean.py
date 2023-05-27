#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Drop cases table."""

    query = 'DROP TABLE IF EXISTS cases'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to drop {db_config.cases} table')
            c.execute(query)
    except Exception as e:
        raise Exception(f'Failed to drop {db_config.cases} table') from e
    else: # no exception
        print(f'Dropped {db_config.cases} table')
    finally:
        c.close()
        cnx.close()
